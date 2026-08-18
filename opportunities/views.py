from django.shortcuts import render
from .models import Opportunity

def home(request):
    """Display the main landing page for the Community Volunteering Hub"""
    opportunities = Opportunity.objects.filter(is_active=True).order_by("-date")
    context = {
        "opportunities": opportunities,
    }
    return render(request, "opportunities/home.html", context)
