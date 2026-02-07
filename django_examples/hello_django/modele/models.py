from django.db import models


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Person(TimeStampedModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True)
    is_active = models.BooleanField(default=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Instructor(Person):
    CONTRTACT_TYPE_CHOICES = (
        ('full', 'Full-time'),
        ('part', 'Part-time')
    )
    hire_date = models.DateField(null=True)
    bio = models.TextField(null=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True)
    contract_type = models.CharField(choices=CONTRTACT_TYPE_CHOICES, max_length=5, null=True)


class Department(TimeStampedModel):
    name = models.CharField(max_length=100)
    description = models.TextField(null=True)
    is_active = models.BooleanField(default=True)
    chair = models.ForeignKey(
        Instructor,
        on_delete=models.SET_NULL,
        null=True,
        related_name='departments'
    )
