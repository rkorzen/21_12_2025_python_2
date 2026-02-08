from django.contrib import admin
from modele.models import Instructor, Department
# Register your models here.

@admin.register(Instructor)
class InstructorAdmin(admin.ModelAdmin):
    pass

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    pass