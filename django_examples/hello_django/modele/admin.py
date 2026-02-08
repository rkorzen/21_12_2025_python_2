from django.contrib import admin
from modele.models import Instructor
# Register your models here.

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    pass