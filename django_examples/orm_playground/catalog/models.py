from decimal import Decimal
from django.db import models
from django.db.models import Q, OuterRef, Subquery, Value
from django.core.validators import MinValueValidator
from django.db.models.functions import Coalesce

# Create your models here.
from core.models import TimeStampedModel


class Category(TimeStampedModel):
    """Kategoria produktu w drzewie (root + children)"""

    name = models.CharField(max_length=120)
    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="children"
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=["name", "parent"], name="uniq_category_name_parent")
        ]
        indexes = [
            models.Index(fields=['name'], name="category_name_idx")
        ]

    def __str__(self):
        return self.name


class Tag(TimeStampedModel):
    name = models.CharField(max_length=64, unique=True)

    def __str__(self):
        return self.name


class ProductQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_active=True)

    def with_latest_inventory_qty(self):
        """Adnotuje produkt najnowsza znana iloscia dostepna w magazynie"""
        latest_snapshot = (
            InventorySnapshot.objects.filter(sku=OuterRef("sku"))
            .order_by("-captured_at")
            .values('available_qty')[:1]
        )

        return self.annotate(
            latest_inventory_qty=Coalesce(
                Subquery(latest_snapshot),
                Value(0)
            )
        )


class Product(TimeStampedModel):
    sku = models.CharField(max_length=40, unique=True)
    name = models.CharField(max_length=180)

    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="products")
    tags = models.ManyToManyField(Tag, related_name="products", blank=True)
    base_price = models.DecimalField(max_digits=12, decimal_places=2)
    country_code = models.CharField(max_length=2)
    source_system_id = models.CharField(max_length=40, default="PIM")
    is_active = models.BooleanField(default=True)

    objects = ProductQuerySet.as_manager()

    class Meta:
        indexes = [
            models.Index(fields=["sku", "country_code"], name="product_sku_country_idx"),
            models.Index(fields=["source_system_id"], name="product_source_idx")
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(base_price__gte=Decimal(0)),  # to sie dzieje na poziomie bazy danych
                name="product_price_non_negative"
            )
        ]

    def __str__(self):
        return f"{self.sku} - {self.name}"


class InventorySnapshot(TimeStampedModel):
    """snapshot stanu magazynu dla SKU w konkretnym momencie czasu"""

    sku = models.CharField(max_length=40)
    captured_at = models.DateTimeField()
    available_qty = models.IntegerField(validators=[MinValueValidator(0)])  # to sie dzieje na poziomie aplikacji
    reserved_qty = models.PositiveIntegerField(default=0)
    warehouse_code = models.CharField(max_length=32)

    class Meta:
        indexes = [
            models.Index(fields=["sku", "-captured_at"], name="inventory_sky_captured_idx"),
            models.Index(fields=["warehouse_code"], name="inventory_wh_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(available_qty__gte=Decimal(0)),  # to sie dzieje na poziomie bazy danych
                name="inventory_available_non_negative"
            ),
            models.CheckConstraint(
                condition=Q(reserved_qty__gte=Decimal(0)),  # to sie dzieje na poziomie bazy danych
                name="inventory_reserved_non_negative"
            )
        ]

    def __str__(self):
        return f"{self.sku} @ {self.captured_at:%Y-%m-%d %H:%M:%S}"