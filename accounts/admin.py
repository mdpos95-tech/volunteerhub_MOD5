from django.contrib import admin
from .models import Application

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("user", "opportunity", "status", "applied_on")
    list_filter = ("status", "applied_on")
    search_fields = ("user__username", "opportunity__title")
    ordering = ("-applied_on",)