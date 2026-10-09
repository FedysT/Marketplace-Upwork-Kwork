from django.conf import settings
from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=80, unique=True)
    slug = models.SlugField(max_length=90, unique=True)
    description = models.CharField(max_length=180, blank=True)

    class Meta:
        ordering = ["name"]

    def __str__(self):
        return self.name

class Service(models.Model):
    freelancer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="services")
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="services")
    title = models.CharField(max_length=140)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    delivery_days = models.PositiveIntegerField(default=3)
    image_url = models.URLField(blank=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.title

    @property
    def image(self):
        return self.image_url or f"https://picsum.photos/seed/service-{self.pk}/900/600"
