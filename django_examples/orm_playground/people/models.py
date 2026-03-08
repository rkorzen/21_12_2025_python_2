from __future__ import annotations

from decimal import Decimal

from django.db import models
from django.db.models import DecimalField, ExpressionWrapper, F, OuterRef, Q, Subquery, Sum, Value
from django.db.models.functions import Coalesce

from core.models import TimeStampedModel


class Organization(TimeStampedModel):
    """Firma/organizacja klienta; jednostka przypisania osób i ról."""

    name = models.CharField(max_length=120)
    country_code = models.CharField(max_length=2)
    source_system_id = models.CharField(max_length=40, default="CRM")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "country_code"],
                name="uniq_organization_name_country",
            )
        ]
        indexes = [
            models.Index(fields=["country_code", "name"], name="org_country_name_idx"),
            models.Index(fields=["source_system_id"], name="org_source_idx"),
        ]

    def __str__(self):
        return f"{self.name} ({self.country_code})"


class Role(TimeStampedModel):
    """Słownik ról biznesowych przypisywanych użytkownikom."""

    code = models.CharField(max_length=40, unique=True)
    label = models.CharField(max_length=120)

    def __str__(self):
        return self.label


class PersonQuerySet(models.QuerySet):
    """Zestaw helperów do filtrowania i agregacji danych o osobach."""

    def active(self):
        """Osoby aktywne, które nie są oznaczone jako usunięte."""
        return self.filter(is_active=True, is_deleted=False)

    def in_country(self, country_code: str):
        """Osoby przypisane do wskazanego kraju."""
        return self.filter(country_code=country_code)

    def with_total_spend(self):
        """Adnotuje osoby łącznym wydatkiem wyliczonym z pozycji zamówień."""
        from sales.models import OrderItem

        spend_subquery = (
            OrderItem.objects.filter(order__customer=OuterRef("pk"))
            .values("order__customer")
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

        return self.annotate(
            total_spend=Coalesce(
                Subquery(spend_subquery),
                Value(Decimal("0.00")),
                output_field=DecimalField(max_digits=14, decimal_places=2),
            )
        )


class Person(TimeStampedModel):
    """Osoba (klient/użytkownik) powiązana z organizacją i strukturą menedżerską."""

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=120)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="people",
    )
    manager = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reports",
    )
    country_code = models.CharField(max_length=2)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    source_system_id = models.CharField(max_length=40, default="CRM")
    joined_at = models.DateField(null=True, blank=True)

    roles = models.ManyToManyField(
        Role,
        through="PersonRole",
        related_name="people",
    )

    # Domyślny manager z czytelnym API domenowym (`active`, `in_country`, `with_total_spend`).
    objects = PersonQuerySet.as_manager()

    class Meta:
        indexes = [
            models.Index(fields=["country_code", "email"], name="person_country_email_idx"),
            models.Index(fields=["source_system_id"], name="person_source_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(email__contains="@"),
                name="person_email_contains_at",
            ),
        ]

    def __str__(self):
        return self.full_name


class PersonRole(TimeStampedModel):
    """Tabela pośrednia M2M: przypisanie roli do osoby w kontekście organizacji."""

    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
        blank=True,
    )
    assigned_at = models.DateField(auto_now_add=True)
    source_system_id = models.CharField(max_length=40, default="IAM")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["person", "role", "organization"],
                name="uniq_person_role_org",
            )
        ]
        indexes = [
            models.Index(fields=["source_system_id"], name="person_role_source_idx"),
        ]

    def __str__(self):
        return f"{self.person_id}:{self.role_id}:{self.organization_id}"
