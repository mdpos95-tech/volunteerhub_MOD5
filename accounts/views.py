from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from .forms import UserUpdateForm, MessageForm
from django.contrib import messages
from django.shortcuts import redirect, render, get_object_or_404

from .models import Application, Message
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

@login_required
def my_applications(request):
    applications = Application.objects.filter(user=request.user).select_related('opportunity').order_by('-applied_on')
    context = {
        "applications": applications,
    }
    return render(request, "accounts/my_applications.html", context)

@login_required
def profile(request):
    if request.method == "POST":
        form = UserUpdateForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Your profile has been updated.")
            return redirect("accounts:profile")
    else:
        form = UserUpdateForm(instance=request.user)
    return render(request, "accounts/profile.html", {"form": form})


@login_required
def inbox(request):
    messages_received = Message.objects.filter(recipient=request.user, archived=False).order_by('-sent_at')
    return render(request, "accounts/inbox.html", {"received_messages": messages_received})

@login_required
def sent_messages(request):
    if request.method == "POST":
        form = MessageForm(request.POST)
        if form.is_valid():
            new_message = form.save(commit=False)
            new_message.sender = request.user
            new_message.save()
            messages.success(request, "Message sent successfully.")
            return redirect("accounts:inbox")

        else: form = MessageForm()
    return render(request, "accounts/send_message.html", {"form": form})

