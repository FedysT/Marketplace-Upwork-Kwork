from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .models import Favorite
from services.models import Service

@login_required
def toggle_favorite(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    favorite, created = Favorite.objects.get_or_create(user=request.user, service=service)
    if not created:
        favorite.delete()
        messages.info(request, "Removed from favorites.")
    else:
        messages.success(request, "Added to favorites.")
    return redirect(request.POST.get("next") or request.META.get("HTTP_REFERER") or "home")

@login_required
def favorite_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related("service", "service__freelancer", "service__category")
    return render(request, "favorites/list.html", {"favorites": favorites})
