from decimal import Decimal
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models
from django.db.models import Q

from core.models import TimeStampedModel


class OrderQuerySet(models.QuerySet):

    def confirmed(self):
        return self.filter(status=Order.Status.CONFIRMED)

    def in_country(self, country_code):
        return self.filter(country_code=country_code)

    def with_order_total(self):
        """Adnotuj zamowienie suma wartosci pozycji (quantity * unit_price

        self.annotate
            order_total
               Coalesce
                 Sum
                  ExpressionWrapper
                   F x F
        """
        raise NotImplementedError()


class Order(TimeStampedModel):

    class Status(models.TextChoices):
        DRAFT = "draft", "Draft"
        CONFIRMED = "confirmed", "Confirmed"
        SHIPPED = "shipped", "Shipped"
        CANCELLED = "cancelled", "Cancelled"

    external_ref = models.CharField(max_length=64, unique=True)
    customer = models.ForeignKey("people.Person", on_delete=models.PROTECT, related_name="orders")
    status = models.CharField(max_length=16, choices=Status.choices, default=Status.DRAFT)
    country_code = models.CharField(max_length=2)
    source_system_id = models.CharField(max_length=40, default="OMS")

    objects = OrderQuerySet.as_manager()

    class Meta:
        indexes = [
            models.Index(fields=["created_at", "status"], name="order_created_status_idx"),
            models.Index(fields=["source_system_id"], name='order_source_idx')
        ]
        constraints = [
            models.CheckConstraint(
                condition=~Q(external_ref=""),
                name="order_external_ref_not_empty"
            )
        ]

    def __str__(self):
        return self.external_ref


class OrderItem(TimeStampedModel):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="items")
    product = models.ForeignKey(
        "catalog.Product",
        on_delete=models.PROTECT,
        related_name="order_items"
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=12, decimal_places=2)
    discount_pct = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=Decimal("0.00"),
        validators=[
            MinValueValidator(Decimal("0")),
            MaxValueValidator(Decimal("100"))
        ]
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["order", "product"], name="uniq_order_product"),
            models.CheckConstraint(condition=Q(quantity__gt=0), name="orderitem_quantity_gt_zero"),
            models.CheckConstraint(condition=Q(unit_price__gte=0), name="orderitem_price_non_negative"),
            models.CheckConstraint(
                condition=Q(discount_pct__gte=0) & Q(discount_pct__lte=100),
                name="orderitem_discount_betweem_0_and_100"),
        ]
        indexes = [
            models.Index(fields=["order", "product"])
        ]

    def __str__(self):
        return f"Order {self.order_id} / Product {self.product_id}"

class Payment(TimeStampedModel):

    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        FAILED = "failed", "Failed"

    external_order_ref = models.CharField(max_length=64)
    status = models.CharField(max_length=12, choices=Status.choices, default=Status.PENDING)
    amount = models.DecimalField(max_digits=12, decimal_places=2)
    paid_at = models.DateTimeField(null=True, blank=True)
    provider = models.CharField(max_length=32)
    transaction_id = models.CharField(max_length=64, unique=True)
    source_system_id = models.CharField(max_length=40, default='PSP')

    class Meta:
        indexes = [
            models.Index(fields=["external_order_ref", "status"]),
            models.Index(fields=["paid_at"]),
            models.Index(fields=["source_system_id"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(amount__gte=0),
                name="payment_amount_non_negative"
            ),
            models.CheckConstraint(
                condition=~Q(external_order_ref=""),
                name="payment_external_ref_not_empty"
            )

        ]

    def __str__(self):
        return f"{self.external_order_ref}:{self.status}"