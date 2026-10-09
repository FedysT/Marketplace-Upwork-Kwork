from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from .forms import ReviewForm
from .models import Review
from orders.models import Order

@login_required
def create_review(request, order_id):
    order = get_object_or_404(Order.objects.select_related("service", "freelancer"), pk=order_id, customer=request.user)
    if order.status != Order.Status.COMPLETED:
        messages.error(request, "You can review a completed order only.")
        return redirect("order_detail", pk=order.pk)
    if hasattr(order, "review"):
        return redirect("order_detail", pk=order.pk)
    form = ReviewForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        review = form.save(commit=False)
        review.order = order
        review.customer = request.user
        review.freelancer = order.freelancer
        review.service = order.service
        review.save()
        messages.success(request, "Thanks for your review.")
        return redirect("order_detail", pk=order.pk)
    return render(request, "reviews/form.html", {"form": form, "order": order})
