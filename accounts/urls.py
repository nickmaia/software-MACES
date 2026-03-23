from django.urls import path

from .views import UserCreate, LoginView, LogoutView, update_profile

urlpatterns = [
    path("register/", UserCreate.as_view(), name="register"),
    path("login/", LoginView.as_view(), name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("profile/update/", update_profile, name="update_profile"),
]
