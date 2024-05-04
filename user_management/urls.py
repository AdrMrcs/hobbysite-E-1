from django.urls import path
from .views import ProfileUpdateView, register


urlpatterns = [
    path("", ProfileUpdateView.as_view(), name="profile-update"),
    path("register", register, name="register"),
]

app_name = "user_management"