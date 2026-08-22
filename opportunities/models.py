from django.db import models

class Opportunity(models.Model):
    CATEGORY_CHOICES = [
        ("environment", "Environment"),
        ("education", "Education"),
        ("community", "Community"),
        ("charity", "Charity"),
        ("food", "Food Support"),
        ("other", "Other"),
    ]
    category = models.CharField(max_length=20, choices=CATEGORY_CHOICES, default="community")

    title = models.CharField(max_length=200)
    organization = models.CharField(max_length=150)
    location = models.CharField(max_length=150)
    description = models.TextField()
    date = models.DateField()
    spaces_available = models.PositiveIntegerField(default=1)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Opportunities"

    def __str__(self):
        return self.title

