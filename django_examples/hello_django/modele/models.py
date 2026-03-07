from django.db import models
from django.utils import timezone

class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Person(TimeStampedModel):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    birth_date = models.DateField(null=True, blank=True)
    is_active = models.BooleanField(default=True)

    @property
    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Instructor(Person):
    CONTRTACT_TYPE_CHOICES = (
        ('full', 'Full-time'),
        ('part', 'Part-time')
    )
    hire_date = models.DateField(null=True, blank=True)
    bio = models.TextField(null=True, blank=True)
    salary = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    contract_type = models.CharField(choices=CONTRTACT_TYPE_CHOICES, max_length=5, null=True, blank=True)


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


class Student(Person):
    enrollment_date = models.DateField(null=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name})"


class Enrollment(TimeStampedModel):
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    course = models.ForeignKey("Course", on_delete=models.CASCADE)
    grade = models.DecimalField(max_digits=3, decimal_places=2, null=True)


class CourseQuerySet(models.QuerySet):
    def active(self):
        return self.filter(is_published=True, department__is_active=True)

    def upcoming(self):
        today = timezone.now().date()
        return self.filter(start_date__gte=today)

    def with_department(self):
        return self.select_related("department")

class CourseManager(models.Manager.from_queryset(CourseQuerySet)):
    pass

CourseQuerySet.as_manager()

class Course(TimeStampedModel):
    class Level(models.TextChoices):
        BEGINNER = 'BEG', 'Beginner'
        INTERMEDIATE = 'INT', 'Intermediate'
        ADVANCED = 'ADV', 'Advanced'

    title = models.CharField(max_length=100)
    summary = models.TextField(null=True)
    department = models.ForeignKey(Department, on_delete=models.PROTECT)

    start_date = models.DateField()
    end_date = models.DateField(null=True)

    is_published = models.BooleanField(default=False)
    level = models.CharField(max_length=10, choices=Level.choices)
    max_students = models.PositiveIntegerField(default=20)

    students = models.ManyToManyField(Student, through='Enrollment', related_name="courses")

    custom_manager = CourseManager()
    objects = CourseQuerySet.as_manager()

    def __str__(self):
        return f"{self.title} ({self.department.name} - {self.get_level_display()}) - {self.start_date})"

    # class Meta:
    #     indexes = [
    #         models.Index(fields=['start_date'], name='start_date_index'),
    #         models.Index(fields=['end_date'], name='end_date_index'),
    #     ]
    #
    #     constraints = [
    #         models.UniqueConstraint(
    #             fields=['department', 'start_date'],
    #         ),
    #         models.CheckConstraint(
    #             condition=models.Q(start_date__lte=timezone.now()),
    #         )
    #     ]
    #