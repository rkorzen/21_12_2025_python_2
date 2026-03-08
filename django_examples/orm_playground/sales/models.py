from __future__ import annotations

from decimal import Decimal

from django.db import models
from django.db.models import DecimalField, ExpressionWrapper, F, Q, Sum, Value
from django.db.models.functions import Coalesce

from core.models import TimeStampedModel


class OrderQuerySet(models.QuerySet):
    """Helpery filtrowania i agregacji dla zamówień sprzedażowych."""

    def confirmed(self):
        """Zamówienia poza statusem anulowanym."""
        return self.exclude(status=Order.Status.CANCELLED)

    def in_country(self, country_code: str):
        """Zamówienia utworzone dla wskazanego kraju."""
        return self.filter(country_code=country_code)

    def with_order_total(self):
        """Adnotuje zamówienie sumą wartości pozycji (quantity * unit_price)."""
        return self.annotate(
            order_total=Coalesce(
                Sum(
                    ExpressionWrapper(
                        F("items__quantity") * F("items__unit_price"),
                        output_field=DecimalField(max_digits=14, decimal_places=2),
                    )
                ),
                Value(Decimal("0.00")),
                output_field=DecimalField(max_digits=14, decimal_places=2),
            )
        )


class Order(TimeStampedModel):
    """Nagłówek zamówienia klienta; centralny rekord procesu sprzedaży."""

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        CONFIRMED = "confirmed", "Confirmed"
        SHIPPED = "shipped", "Shipped"
        CANCELLED = "cancelled", "Cancelled"

    external_ref = models.CharField(max_length=64, unique=True)
    customer = models.ForeignKey("people.Person", on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.CONFIRMED)
    country_code = models.CharField(max_length=2)
    source_system_id = models.CharField(max_length=40, default="OMS")

    # Manager zapewniający API domenowe (`confirmed`, `in_country`, `with_order_total`).
    objects = OrderQuerySet.as_manager()

    class Meta:
        indexes = [
            models.Index(fields=["created_at", "status"], name="order_created_status_idx"),
            models.Index(fields=["source_system_id"], name="order_source_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=~Q(external_ref=""),
                name="order_external_ref_not_empty",
            )
        ]

    def __str__(self):
        return self.external_ref


class OrderItem(TimeStampedModel):
    """Pozycja zamówienia: produkt, ilość, cena i rabat."""

    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.PROTECT,
        related_name="order_items",
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_pct = models.DecimalField(max_digits=5, decimal_places=2, default=Decimal("0.00"))

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["order", "product"], name="uniq_order_product"),
            models.CheckConstraint(condition=Q(quantity__gt=0), name="orderitem_quantity_gt_zero"),
            models.CheckConstraint(
                condition=Q(unit_price__gte=0),
                name="orderitem_price_non_negative",
            ),
            models.CheckConstraint(
                condition=Q(discount_pct__gte=0) & Q(discount_pct__lte=100),
                name="orderitem_discount_between_0_100",
            ),
        ]
        indexes = [
            models.Index(fields=["order", "product"], name="orderitem_order_product_idx"),
        ]

    def __str__(self):
        return f"Order {self.order_id} / Product {self.product_id}"


class Payment(TimeStampedModel):
    """Zdarzenie płatnicze powiązane z zamówieniem przez external reference."""

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"

    external_order_ref = models.CharField(max_length=64)
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.PENDING)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_at = models.DateTimeField(null=True, blank=True)
    provider = models.CharField(max_length=32)
    transaction_id = models.CharField(max_length=64, unique=True)
    source_system_id = models.CharField(max_length=40, default="PSP")

    class Meta:
        indexes = [
            models.Index(fields=["external_order_ref", "status"], name="payment_extref_status_idx"),
            models.Index(fields=["paid_at"], name="payment_paid_at_idx"),
            models.Index(fields=["source_system_id"], name="payment_source_idx"),
        ]
        constraints = [
            models.CheckConstraint(condition=Q(amount__gte=0), name="payment_amount_non_negative"),
            models.CheckConstraint(
                condition=~Q(external_order_ref=""),
                name="payment_extref_not_empty",
            ),
        ]

    def __str__(self):
        return f"{self.external_order_ref}:{self.status}"
