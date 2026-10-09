from django.contrib import admin
from .models import Order

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "service", "customer", "freelancer", "price", "status", "created_at"]
    list_filter = ["status"]
    search_fields = ["service__title", "customer__username", "freelancer__username"]
