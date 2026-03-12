from django.contrib import admin
from .models import ParishGroup

@admin.register(ParishGroup)
class ParishGroupAdmin(admin.ModelAdmin):
    list_display = ("name", "leader")
    search_fields = ("name", "leader__username")