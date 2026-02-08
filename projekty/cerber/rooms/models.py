from django.core.exceptions import ValidationError
from django.db import models
from django.utils import timezone
# Create your models here.

class Room(models.Model):
    name = models.CharField(max_length=200, unique=True)
    location = models.CharField(max_length=200, blank=True)
    capacity = models.IntegerField(default=10)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name


class Reservation(models.Model):

    class Status(models.TextChoices):
        ACTIVE = "active", "Active"
        CANCELLED = "cancelled", "Cancelled"

    room = models.ForeignKey(Room, on_delete=models.PROTECT, related_name='reservations')
    organizer = models.ForeignKey('auth.User', on_delete=models.PROTECT, related_name='reservations')

    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    start_at = models.DateTimeField()
    end_at = models.DateTimeField()

    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)

    canceled_at = models.DateTimeField(blank=True, null=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['start_at']

        indexes = [
            models.Index(fields=['room', 'start_at', 'end_at'], name='res_room_start_end_idx'),
            models.Index(fields=['organizer', 'start_at'], name='res_organizer_start_idx'),
        ]

    def __str__(self):
        return f"{self.title} = {self.room}"


    def clean(self):
        errors = {}
        if self.start_at >= self.end_at:
            errors['start_at'] = "Start time must be before end time."

        if self.start_at < timezone.now():
            errors['start_at'] = "Reservation start time must be in the future."

        conflicts = Reservation.objects.filter(
            room=self.room, start_at__range=(self.start_at, self.end_at)
        )
        if self.pk:
            conflicts = conflicts.exclude(pk=self.pk)
        if conflicts.exists():
            errors['__all__'] = "Reservation conflicts with another reservation."

        if errors:
            raise ValidationError(errors)

    def cancel(self):
        if self.status == Reservation.Status.CANCELLED:
            return
        self.status = Reservation.Status.CANCELLED
        self.canceled_at = timezone.now()
        self.save(update_fields=["status", "canceled_at"])