from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from .forms import OrderStatusForm
from .models import Order
from services.models import Service

@login_required
def create_order(request, service_id):
    service = get_object_or_404(Service, pk=service_id, is_active=True)
    if service.freelancer_id == request.user.id:
        messages.error(request, "You cannot order your own service.")
        return redirect("service_detail", pk=service.pk)
    if request.user.role != "CUSTOMER":
        messages.error(request, "Only customers can place orders.")
        return redirect("service_detail", pk=service.pk)
    if request.method == "POST":
        order = Order.objects.create(
            customer=request.user,
            freelancer=service.freelancer,
            service=service,
            price=service.price,
        )
        messages.success(request, f"Order #{order.pk} has been created.")
        return redirect("order_detail", pk=order.pk)
    return redirect("service_detail", pk=service.pk)

@login_required
def order_list(request):
    if request.user.role == "FREELANCER":
        orders = Order.objects.filter(freelancer=request.user).select_related("customer", "service")
    else:
        orders = Order.objects.filter(customer=request.user).select_related("freelancer", "service")
    status = request.GET.get("status", "")
    if status:
        orders = orders.filter(status=status)
    return render(request, "orders/list.html", {"orders": orders, "status": status, "statuses": Order.Status.choices})

@login_required
def order_detail(request, pk):
    order = get_object_or_404(Order.objects.select_related("customer", "freelancer", "service"), pk=pk)
    if request.user not in [order.customer, order.freelancer]:
        return redirect("home")
    form = None
    if request.user == order.freelancer and order.status not in [Order.Status.COMPLETED, Order.Status.CANCELLED]:
        form = OrderStatusForm(request.POST or None, instance=order)
        if request.method == "POST" and form.is_valid():
            form.save()
            messages.success(request, "Order status updated.")
            return redirect("order_detail", pk=order.pk)
    return render(request, "orders/detail.html", {"order": order, "status_form": form})

@login_required
def cancel_order(request, pk):
    order = get_object_or_404(Order, pk=pk, customer=request.user)
    if order.status in [Order.Status.PENDING, Order.Status.ACCEPTED]:
        order.status = Order.Status.CANCELLED
        order.save(update_fields=["status", "updated_at"])
        messages.success(request, "Order cancelled.")
    return redirect("order_detail", pk=order.pk)
