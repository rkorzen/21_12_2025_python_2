from django.contrib.contenttypes.fields import GenericForeignKey
from django.db import models

from core.models import TimeStampedModel


# Create your models here.


class EventLogQuerySet(models.QuerySet):
    def with_actor_match(self):
        raise NotImplementedError


class EventLog(TimeStampedModel):

    class EventType(models.TextChoices):
        LOGIN = "login", "Login"
        ORDER_PLACED = "order_placed", "Order Places"
        PAYMENT_UPDATED = "payment_updated", "Payment Updated"
        PROFILE_UPDATED = "profile_update", "Profile Update"

    actor_email = models.EmailField(blank=True)
    event_type = models.CharField(max_length=32, choices=EventType.choices)
    happened_at = models.DateTimeField()
    payload = models.JSONField(default=dict, blank=True)
    country_code = models.CharField(max_length=2, default="US")
    source_system_id = models.CharField(max_length=40, default="TRACKER")

    content_type = models.ForeignKey("contenttypes.ContentType", null=True, blank=True, on_delete=models.SET_NULL)
    object_id = models.PositiveBigIntegerField(null=True, blank=True)
    content_object = GenericForeignKey("content_type", "object_id")

    objects = EventLogQuerySet.as_manager()


    def __str__(self):
        return f"{self.event_type}" @ {self.happened_at.isoformat()}