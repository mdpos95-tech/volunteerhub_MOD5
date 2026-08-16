from django.shortcuts import render

# Create your views here.
def home(request):
    """Display the main landing page for the Community Volunteering Hub"""
    return render(request,"opportunities/home.html")
