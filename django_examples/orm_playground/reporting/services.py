"""Warstwa zapytań ORM dla raportów.

Każda funkcja zwraca queryset lub serializowalną strukturę danych, której
używają endpointy JSON i strony HTML w `reporting/views.py`.
"""

from __future__ import annotations

from datetime import timedelta
from decimal import Decimal

from django.db import connection
from django.db.models import (
    Avg,
    BooleanField,
    Case,
    Count,
    DateTimeField,
    DecimalField,
    Exists,
    ExpressionWrapper,
    F,
    FilteredRelation,
    OuterRef,
    Prefetch,
    Q,
    Subquery,
    Sum,
    Value,
    When,
    Window,
)
from django.db.models.functions import Coalesce, Rank, RowNumber
from django.test.utils import CaptureQueriesContext
from django.utils import timezone

from events.models import EventLog
from people.models import Person
from sales.models import Order, OrderItem, Payment


def paginate_queryset(queryset, page: int, page_size: int):
    """Wykonuje prostą paginację offsetową na dowolnym querysetcie."""
    total = queryset.count()
    start = (page - 1) * page_size
    end = start + page_size
    return total, list(queryset[start:end])


def top_products_queryset(days: int = 30, country: str | None = None):
    """Raport top produktów po przychodzie i wolumenie sprzedaży."""
    since = timezone.now() - timedelta(days=days)
    filters = Q(order__created_at__gte=since)
    if country:
        filters &= Q(order__country_code=country)

    # Liczymy wartość pozycji zamówienia po stronie bazy: quantity * unit_price.
    revenue_expr = ExpressionWrapper(
        F("quantity") * F("unit_price"),
        output_field=DecimalField(max_digits=14, decimal_places=2),
    )

    return (
        OrderItem.objects.filter(filters)
        .values("product__sku", "product__name")
        .annotate(
            total_qty=Coalesce(Sum("quantity"), 0),
            revenue=Coalesce(
                Sum(revenue_expr),
                Value(Decimal("0.00")),
                output_field=DecimalField(max_digits=14, decimal_places=2),
            ),
            order_count=Count("order", distinct=True),
            avg_qty=Coalesce(Avg("quantity"), 0.0),
        )
        .order_by("-revenue", "product__sku")
    )


def customers_ltv_queryset(days: int = 180, country: str | None = None):
    """Raport LTV klientów aktywnych w zadanym okresie."""
    since = timezone.now() - timedelta(days=days)

    order_filters = Q(orders__created_at__gte=since)
    if country:
        order_filters &= Q(orders__country_code=country)

    # Sumujemy wartości pozycji tylko dla relacji `scoped_orders`.
    revenue_expr = ExpressionWrapper(
        F("scoped_orders__items__quantity") * F("scoped_orders__items__unit_price"),
        output_field=DecimalField(max_digits=14, decimal_places=2),
    )

    # FilteredRelation tworzy alias relacji ograniczony warunkiem okres/kraj.
    queryset = Person.objects.active().annotate(
        scoped_orders=FilteredRelation("orders", condition=order_filters)
    )
    if country:
        queryset = queryset.in_country(country)

    return queryset.annotate(
        ltv=Coalesce(
            Sum(revenue_expr),
            Value(Decimal("0.00")),
            output_field=DecimalField(max_digits=14, decimal_places=2),
        ),
        orders_count=Count("scoped_orders", distinct=True),
    ).order_by("-ltv", "id")


def orders_with_late_payment_queryset(
    days: int = 60,
    country: str | None = None,
    grace_days: int = 3,
):
    """Raport zamówień, których pierwsza płatność pojawiła się po progu czasowym."""
    since = timezone.now() - timedelta(days=days)
    # Pseudo-join: Payment.external_order_ref -> Order.external_ref (bez FK).
    payments = Payment.objects.filter(
        external_order_ref=OuterRef("external_ref"),
        status=Payment.Status.PAID,
        paid_at__isnull=False,
    ).order_by("paid_at")

    threshold = ExpressionWrapper(
        F("created_at") + timedelta(days=grace_days),
        output_field=DateTimeField(),
    )

    # `confirmed()` usuwa anulowane zamówienia na poziomie QuerySet API.
    queryset = Order.objects.confirmed().filter(created_at__gte=since)
    if country:
        queryset = queryset.in_country(country)

    return (
        queryset.annotate(
            has_payment=Exists(Payment.objects.filter(external_order_ref=OuterRef("external_ref"))),
            first_paid_at=Subquery(payments.values("paid_at")[:1]),
            first_paid_amount=Subquery(payments.values("amount")[:1]),
            late_payment=Case(
                When(first_paid_at__gt=threshold, then=Value(True)),
                default=Value(False),
                output_field=BooleanField(),
            ),
        )
        .filter(late_payment=True)
        .order_by("-created_at", "external_ref")
    )


def events_matched_by_email_queryset(days: int = 30, country: str | None = None):
    """Raport eventów, które da się dopasować do osoby po e-mailu aktora."""
    since = timezone.now() - timedelta(days=days)
    queryset = EventLog.objects.with_actor_match().filter(happened_at__gte=since)
    if country:
        queryset = queryset.filter(country_code=country)

    return queryset.filter(has_person=True).order_by("-happened_at", "id")


def window_rankings_queryset(days: int = 90):
    """Ranking zamówień z funkcjami okna: rank, row_number i running total."""
    since = timezone.now() - timedelta(days=days)
    # Subquery liczy sumę pozycji dla pojedynczego zamówienia.
    line_total_subquery = (
        OrderItem.objects.filter(order=OuterRef("pk"))
        .values("order")
        .annotate(
            total=Sum(
                ExpressionWrapper(
                    F("quantity") * F("unit_price"),
                    output_field=DecimalField(max_digits=14, decimal_places=2),
                )
            )
        )
        .values("total")[:1]
    )

    return (
        Order.objects.filter(created_at__gte=since)
        .annotate(
            order_total=Coalesce(
                Subquery(line_total_subquery),
                Value(Decimal("0.00")),
                output_field=DecimalField(max_digits=14, decimal_places=2),
            )
        )
        # Funkcje okna działają na już wyliczonym `order_total`.
        .annotate(
            rank=Window(
                expression=Rank(),
                order_by=[F("order_total").desc(), F("id").asc()],
            ),
            row_number=Window(
                expression=RowNumber(),
                order_by=[F("order_total").desc(), F("id").asc()],
            ),
            running_total=Window(
                expression=Sum("order_total"),
                order_by=[F("order_total").desc(), F("id").asc()],
            ),
        )
        .select_related("customer")
        .order_by("row_number")
    )


def _serialize_orders(queryset):
    """Serializuje zamówienia do prostego payloadu demonstracyjnego."""
    payload = []
    for order in queryset:
        items_payload = []
        for item in order.items.all():
            items_payload.append(
                {
                    "sku": item.product.sku,
                    "product": item.product.name,
                    "qty": item.quantity,
                }
            )

        payload.append(
            {
                "order_ref": order.external_ref,
                "customer": order.customer.full_name,
                "organization": order.customer.organization.name,
                "items": items_payload,
            }
        )
    return payload


def serialize_orders_naive(limit: int = 20):
    """Wersja celowo naiwna; pokazuje problem N+1 przy iteracji po relacjach."""
    queryset = Order.objects.order_by("id")[:limit]
    return _serialize_orders(queryset)


def serialize_orders_optimized(limit: int = 20):
    """Wersja zoptymalizowana dzięki select_related + prefetch_related."""
    queryset = (
        # Jeden JOIN dla customer i organization.
        Order.objects.select_related("customer__organization")
        .prefetch_related(
            Prefetch(
                # Dociągamy itemy z produktem w osobnym, ale kontrolowanym zapytaniu.
                "items",
                queryset=OrderItem.objects.select_related("product").order_by("id"),
            )
        )
        .order_by("id")[:limit]
    )
    return _serialize_orders(queryset)


def n_plus_one_demo(limit: int = 20):
    """Porównuje liczbę SQL-i pomiędzy wariantem naiwnym i zoptymalizowanym."""
    with CaptureQueriesContext(connection) as bad_queries:
        bad_payload = serialize_orders_naive(limit=limit)

    with CaptureQueriesContext(connection) as good_queries:
        good_payload = serialize_orders_optimized(limit=limit)

    return {
        "bad_query_count": len(bad_queries),
        "good_query_count": len(good_queries),
        "sample_bad": bad_payload[:3],
        "sample_good": good_payload[:3],
    }
