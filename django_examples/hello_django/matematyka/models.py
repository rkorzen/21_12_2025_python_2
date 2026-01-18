from django.db import models

# Create your models here.
class CalculationHistory(models.Model):
    OPERATIONS = (
        ("add", "addition"),
        ("sub", "substraction"),
        ("mul", "multiplication"),
        ("div", "division"),
    )

    operation = models.CharField(max_length=3, choices=OPERATIONS)
    a = models.IntegerField()
    b = models.IntegerField()
    user = models.ForeignKey("auth.User", on_delete=models.CASCADE, null=True)
    result = models.IntegerField(null=True)
    date = models.DateTimeField(auto_now_add=True)
