from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Application(models.Model):
    STATUS_CHOICES = [
        ("pending", "Pending"),
        ("approved", "Approved"),
        ("rejected", "Rejected")
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="applications")
    opportunity = models.ForeignKey("opportunities.Opportunity", on_delete=models.CASCADE, related_name="applications")
    message = models.TextField(blank=True)
    status = models.CharField(max_length=15, choices=STATUS_CHOICES, default="pending")

    applied_on = models.DateTimeField(auto_now_add=True)
class Meta:
    constraints = [
        models.UniqueConstraint(fields=['user', 'opportunity'], name='unique_application')
    ]    
def __str__(self):
        return f"{self.user.username} - {self.opportunity.title}"

class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sent_messages")
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name="received_messages")
    subject = models.CharField(max_length=200)
    body = models.TextField()
    sent_at = models.DateTimeField(auto_now_add=True)
    archived = models.BooleanField(default=False)

    class Meta:
        ordering = ['-sent_at']
    def __str__(self):
        return f"From: {self.sender.username} To: {self.recipient.username}"