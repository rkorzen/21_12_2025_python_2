from django.contrib import admin
from .models import CalculationHistory

# Register your models here.
@admin.register(CalculationHistory)
class CalculationHistoryAdmin(admin.ModelAdmin):
    list_display = ('date', 'operation',  'a', 'b', 'result', 'user')
    readonly_fields = ('operation', 'a', 'b', 'result', 'user', 'date')
    list_filter = ('operation',)
    search_fields = ("result", "user__username", "date")