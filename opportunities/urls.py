from django.urls import path
from . import views
app_name = "opportunities"
urlpatterns = [
    path("", views.home, name="home"),
    path("opportunity/<int:pk>/", views.opportunity_detail, name="opportunity_detail"),
]