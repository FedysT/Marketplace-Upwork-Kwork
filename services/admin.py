from django.contrib import admin
from .models import Category, Service

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "slug"]
    prepopulated_fields = {"slug": ("name",)}

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ["title", "freelancer", "category", "price", "is_active", "created_at"]
    list_filter = ["category", "is_active"]
    search_fields = ["title", "description", "freelancer__username"]
