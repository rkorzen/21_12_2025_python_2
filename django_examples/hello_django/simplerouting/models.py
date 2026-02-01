from django.db import models

# Create your models here.

class HelloUserNameHistory(models.Model):
    username = models.CharField(max_length=100)
    date_of_use = models.DateTimeField(auto_now_add=True)