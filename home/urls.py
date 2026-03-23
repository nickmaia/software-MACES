# No arquivo urls.py do seu projeto ou app
from django.urls import path
from .views import HomeView, AboutView, ContactView, ServicesView

urlpatterns = [
    path("", HomeView.as_view(), name="hero"),
    path("about/", AboutView.as_view(), name="about"),
    path("contact/", ContactView.as_view(), name="contact"),
    path("services/", ServicesView.as_view(), name="services"),
]
