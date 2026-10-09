from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Avg, Count, Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ServiceForm
from .models import Category, Service

def home(request):
    services = Service.objects.filter(is_active=True).select_related("freelancer", "category").annotate(
        rating=Avg("orders__review__rating"),
        review_count=Count("orders__review")
    )
    q = request.GET.get("q", "").strip()
    category = request.GET.get("category", "").strip()
    min_price = request.GET.get("min_price", "").strip()
    max_price = request.GET.get("max_price", "").strip()
    if q:
        services = services.filter(Q(title__icontains=q) | Q(description__icontains=q) | Q(category__name__icontains=q))
    if category:
        services = services.filter(category__slug=category)
    if min_price:
        services = services.filter(price__gte=min_price)
    if max_price:
        services = services.filter(price__lte=max_price)
    services = services.order_by("-created_at")
    paginator = Paginator(services, 9)
    page_obj = paginator.get_page(request.GET.get("page"))
    return render(request, "home.html", {
        "services": page_obj,
        "categories": Category.objects.all(),
        "selected_category": category,
        "query": q,
        "min_price": min_price,
        "max_price": max_price,
    })

def service_detail(request, pk):
    service = get_object_or_404(Service.objects.select_related("freelancer", "category"), pk=pk, is_active=True)
    reviews = service.orders.filter(status="COMPLETED", review__isnull=False).select_related("customer", "review").order_by("-review__created_at")
    is_favorite = request.user.is_authenticated and service.favorites.filter(user=request.user).exists()
    return render(request, "services/detail.html", {"service": service, "reviews": reviews, "is_favorite": is_favorite})

def category_list(request):
    categories = Category.objects.annotate(service_count=Count("services", filter=Q(services__is_active=True)))
    return render(request, "services/categories.html", {"categories": categories})

@login_required
def create_service(request):
    if request.user.role != "FREELANCER":
        messages.error(request, "Only freelancers can create services.")
        return redirect("home")
    form = ServiceForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        service = form.save(commit=False)
        service.freelancer = request.user
        service.save()
        messages.success(request, "Your service has been published.")
        return redirect("service_detail", pk=service.pk)
    return render(request, "services/form.html", {"form": form, "page_title": "Create a service"})

@login_required
def edit_service(request, pk):
    service = get_object_or_404(Service, pk=pk, freelancer=request.user)
    form = ServiceForm(request.POST or None, instance=service)
    if request.method == "POST" and form.is_valid():
        form.save()
        messages.success(request, "Service updated.")
        return redirect("service_detail", pk=service.pk)
    return render(request, "services/form.html", {"form": form, "page_title": "Edit service", "service": service})

@login_required
def my_services(request):
    if request.user.role != "FREELANCER":
        return redirect("home")
    services = request.user.services.select_related("category")
    return render(request, "services/my_services.html", {"services": services})
