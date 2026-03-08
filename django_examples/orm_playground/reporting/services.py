from datetime import timedelta
from decimal import Decimal

from django.db.models import Q, ExpressionWrapper, F, Sum, Value, Count, Avg
from django.db.models.functions import Coalesce
from django.utils import timezone
from django.db.models import DecimalField

from sales.models import OrderItem


class MyDecimalField(DecimalField):
    def __init__(
            self,
            verbose_name=None,
            name=None,
            max_digits=14,
            decimal_places=2,
            **kwargs,
    ):
        super().__init__(verbose_name=verbose_name, name=name, max_digits=max_digits, decimal_places=decimal_places)


def top_products_queryset(days: int = 30, country: str | None = None):
    """
    raport top produktow po przychodzie i wolumenie sprzedazy

    """
    since = timezone.now() - timedelta(days=days)
    filters = Q(order__created_at__gte=since)
    if country:
        filters &= Q(order__country_code=country)

    # liczymy wartosc pozycji zamowienia po stronie bazy:
    # quantity * unit_price

    revenue_expr = ExpressionWrapper(
        F("quantity") * F("unit_price"),
        output_field=MyDecimalField()
    )

    return (
        OrderItem.objects.filter(filters)
        .values("product__sku", "product__name")
        .annotate(
            total_qty=Coalesce(Sum("quantity"), 0),
            revenue=Coalesce(
                Sum(revenue_expr),
                Value(Decimal("0.0")),
                output_field=MyDecimalField()
            ),
            order_count=Count("order", distinct=True),
            avg_qty=Coalesce(Avg("quantity"), 0.0)
        )
        .order_by("-revenue", "product__sku")
    )
