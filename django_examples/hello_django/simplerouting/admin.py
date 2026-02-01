from django.contrib import admin
from .models import HelloUserNameHistory

# Register your models here.
@admin.register(HelloUserNameHistory)
class HelloUserNameHistoryAdmin(admin.ModelAdmin):
    list_display = ('date_of_use', 'username')
    readonly_fields = ('username', 'date_of_use')
    search_fields = ("username",)
