from django.conf import settings
from django.db import models
from services.models import Service

class Favorite(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="favorites")
    service = models.ForeignKey(Service, on_delete=models.CASCADE, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [models.UniqueConstraint(fields=["user", "service"], name="unique_user_service_favorite")]
        ordering = ["-created_at"]

    def __str__(self):
        return f"{self.user.username} - {self.service.title}"
