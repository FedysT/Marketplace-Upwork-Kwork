from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Avg
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ProfileForm, RegisterForm
from .models import User
from orders.models import Order
from reviews.models import Review

def register(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = RegisterForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("home")
    return render(request, "accounts/register.html", {"form": form})

def login_view(request):
    if request.user.is_authenticated:
        return redirect("home")
    form = AuthenticationForm(request, data=request.POST or None)
    if request.method == "POST" and form.is_valid():
        login(request, form.get_user())
        return redirect("home")
    return render(request, "accounts/login.html", {"form": form})

def logout_view(request):
    logout(request)
    return redirect("home")

def profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    services = profile_user.services.filter(is_active=True).select_related("category")
    reviews = Review.objects.filter(freelancer=profile_user).select_related("customer", "service")[:8]
    completed = Order.objects.filter(freelancer=profile_user, status=Order.Status.COMPLETED).count()
    average = Review.objects.filter(freelancer=profile_user).aggregate(value=Avg("rating"))["value"] or 0
    return render(request, "accounts/profile.html", {
        "profile_user": profile_user,
        "services": services,
        "reviews": reviews,
        "completed": completed,
        "average": average,
    })

@login_required
def edit_profile(request):
    form = ProfileForm(request.POST or None, instance=request.user)
    if request.method == "POST" and form.is_valid():
        form.save()
        return redirect("profile", username=request.user.username)
    return render(request, "accounts/profile_form.html", {"form": form})
