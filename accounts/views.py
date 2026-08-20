from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

from .models import Application
from opportunities.models import Opportunity


def register(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get("username")
            messages.success(request, f"Account created for {username}!. You can now log in.")
            return redirect("accounts:login")
    else:
        form = UserCreationForm()
    return render(request, "accounts/register.html", {"form": form})    

@login_required
def apply_for_opportunity(request, opportunity_id):

    opportunity = get_object_or_404(Opportunity, id=opportunity_id, is_active=True)
    application, created = Application.objects.get_or_create(
        user=request.user,
        opportunity=opportunity,
    )
    if created: 
        messages.success(request, f"You have successfully applied for {opportunity.title}.")
    else:
        messages.info(request, f"You have already applied for {opportunity.title}.")
    return redirect("opportunities:opportunity_detail", pk=opportunity_id)

