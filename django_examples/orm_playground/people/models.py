from decimal import Decimal

from django.db import models
from django.db.models import OuterRef, Sum, F, Subquery, Value, ExpressionWrapper
from django.db.models.functions import Coalesce


from core.models import TimeStampedModel


class Organization(TimeStampedModel):
    """
    Firma/organizacja klienta; jednostka przypisania ról i osób.
    """

    name = models.CharField(max_length=120)
    country_code = models.CharField(max_length=2)
    source_system_id = models.CharField(max_length=40, default="CRM")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["name", "country_code"],
                name="uniq_organization_name_country"
            )
        ]
        indexes = [
            models.Index(fields=["country_code", "name"], name="org_country_name_idx"),
            models.Index(fields=["source_system_id"], name="org_source_idx")
        ]

    def __str__(self):
        return f"{self.name} ({self.country_code})"


class Role(TimeStampedModel):

    code = models.CharField(max_length=40, unique=True)
    label = models.CharField(max_length=120)

    def __str__(self):
        return self.label



class PersonQuerySet(models.QuerySet):

    def active(self):
        return self.filter(is_active=True, is_deleted=False)

    def in_country(self, country_code: str):
        return self.filter(country_code=country_code)

    def with_total_spend(self):
        """adnotuj osoby lacznym wydatkiem wyliczonym z pozycji zamowien"""
        from sales.models import OrderItem
        spend_subquery = (
            OrderItem.objects.filter(order__customer=OuterRef("pk"))
            .values("order__customer")
            .annotate(
                total=Sum(
                    ExpressionWrapper(
                        F("quantity") * F("unit_price"),
                        output_field=models.DecimalField(max_digits=14, decimal_places=2)
                    )
                )
            ).values("total")[:1]
        )

        return self.annotate(
            total_spend=Coalesce(
                Subquery(spend_subquery),
                Value(Decimal("0.00")),
                output_field=models.DecimalField(max_digits=14, decimal_places=2)
            )
        )



class Person(TimeStampedModel):
    """
    Osoba (klient/uzytkownik) powiazana z organizacja i struktura managerska
    """

    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=120)
    organization = models.ForeignKey(
        Organization,
        on_delete=models.PROTECT,
        related_name="people"
    )
    manager = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="reports"
    )
    country_code = models.CharField(max_length=2)
    is_active = models.BooleanField(default=True)
    is_deleted = models.BooleanField(default=False)
    source_system_id = models.CharField(max_length=40, default="CRM")
    joined_at = models.DateField(null=True, blank=True)
    roles = models.ManyToManyField(
        Role,
        through="PersonRole",
        related_name="people"
    )

    class Meta:
        indexes = [
            models.Index(fields=["country_code", "email"], name="person_country_email_idx"),
            models.Index(fields=["source_system_id"], name="person_source_idx")
        ]


    objects = PersonQuerySet.as_manager()

    def __str__(self):
        return self.full_name

class PersonRole(TimeStampedModel):
    """Przypisane roli do osoby w kontekscie organizacji"""
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    role = models.ForeignKey(Role, on_delete=models.CASCADE)

    organization = models.ForeignKey(
        Organization,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    assigned_at = models.DateField(auto_now_add=True)
    source_system_id = models.CharField(max_length=40, default="IAM")

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["person", "role", "organization"],
                name="uniq_person_role_org"
            )
        ]
        indexes = [
            models.Index(fields=["source_system_id"], name="person_role_source_idx")
        ]

    def __str__(self):
        return f"{self.person_id}:{self.role_id}:{self.organization_id}"