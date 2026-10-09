from django.urls import path
from .views import edit_profile, login_view, logout_view, profile, register

urlpatterns = [
    path("register/", register, name="register"),
    path("login/", login_view, name="login"),
    path("logout/", logout_view, name="logout"),
    path("profile/edit/", edit_profile, name="edit_profile"),
    path("profile/<str:username>/", profile, name="profile"),
]
