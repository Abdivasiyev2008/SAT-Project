from django.contrib import admin
from .models import Practice

@admin.register(Practice)
class PracticeAdmin(admin.ModelAdmin):
    list_display = ('name', 'start_date')
    search_fields = ('name',)
