from django.contrib import admin
from .models import Opportunity

@admin.register(Opportunity)
class OpportunityAdmin(admin.ModelAdmin):
    list_display = ("title", "organization", "location", "date", "spaces_available", "is_active")
    list_filter = ("is_active", "date")
    search_fields = ("title", "organization", "location")
    ordering = ("-date",)


