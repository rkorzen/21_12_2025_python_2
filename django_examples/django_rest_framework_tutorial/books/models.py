from django.db import models

# Create your models here.

class Book(models.Model):

    class Status(models.TextChoices):
        AVAILABLE = 'av', 'Available'
        RENT = 're', 'Rent'
        ARCHIVED = 'ar', 'Archived'


    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    status = models.CharField(
        max_length=2,
        choices=Status.choices,
        default=Status.AVAILABLE
    )
    visible = models.BooleanField(default=True)
    created = models.DateTimeField(auto_now_add=True)

