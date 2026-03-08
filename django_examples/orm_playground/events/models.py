from __future__ import annotations

from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import Exists, OuterRef, Q, Subquery

from core.models import TimeStampedModel


class EventLogQuerySet(models.QuerySet):
    """QuerySet do wzbogacania logów zdarzeń o dopasowanie aktora do osoby."""

    def with_actor_match(self):
        """Adnotuje log informacją, czy actor_email odpowiada rekordowi Person."""
        from people.models import Person

        matching_people = Person.objects.filter(email=OuterRef("actor_email"))
        return self.annotate(
            has_person=Exists(matching_people),
            matched_person_id=Subquery(matching_people.values("id")[:1]),
            matched_person_name=Subquery(matching_people.values("full_name")[:1]),
        )


class EventLog(TimeStampedModel):
    """Techniczny log zdarzeń z opcjonalnym powiązaniem do dowolnego obiektu."""

    class EventType(models.TextChoices):
        LOGIN = "login", "Login"
        ORDER_PLACED = "order_placed", "Order Placed"
        PAYMENT_UPDATED = "payment_updated", "Payment Updated"
        PROFILE_UPDATED = "profile_updated", "Profile Updated"

    actor_email = models.EmailField(blank=True)
    event_type = models.CharField(max_length=32, choices=EventType.choices)
    happened_at = models.DateTimeField()
    payload = models.JSONField(default=dict, blank=True)
    country_code = models.CharField(max_length=2, default="US")
    source_system_id = models.CharField(max_length=40, default="TRACKER")

    content_type = models.ForeignKey(ContentType, null=True, blank=True, on_delete=models.SET_NULL)
    object_id = models.PositiveBigIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")

    # Manager rozszerzony o helper adnotujący dopasowanie po e-mailu aktora.
    objects = EventLogQuerySet.as_manager()

    class Meta:
        indexes = [
            models.Index(fields=["actor_email", "happened_at"], name="event_actor_happened_idx"),
            models.Index(fields=["event_type", "happened_at"], name="event_type_happened_idx"),
            models.Index(fields=["source_system_id"], name="event_source_idx"),
        ]
        constraints = [
            models.CheckConstraint(
                condition=Q(actor_email="") | Q(actor_email__contains="@"),
                name="event_actor_email_blank_or_email",
            )
        ]

    def __str__(self):
        return f"{self.event_type} @ {self.happened_at:%Y-%m-%d %H:%M:%S}"
