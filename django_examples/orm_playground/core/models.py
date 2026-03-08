from django.db import models
from django.utils import timezone


class TimeStampedModel(models.Model):
    """Abstrakcyjna baza z polami audytowymi `created_at` i `updated_at`."""

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class SoftDeleteQuerySet(models.QuerySet):
    """QuerySet wspierający miękkie usuwanie rekordów przez flagę `is_deleted`."""

    def alive(self):
        """Zwraca tylko rekordy aktywne (nieoznaczone jako usunięte)."""
        return self.filter(is_deleted=False)

    def deleted(self):
        """Zwraca tylko rekordy oznaczone jako usunięte logicznie."""
        return self.filter(is_deleted=True)

    def soft_delete(self):
        """Ustawia flagę `is_deleted=True` bez fizycznego kasowania wierszy."""
        return self.update(is_deleted=True)


class SoftDeleteManager(models.Manager):
    """Domyślny manager ukrywający rekordy miękko usunięte."""

    def get_queryset(self):
        return SoftDeleteQuerySet(self.model, using=self._db).alive()
