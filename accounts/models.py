from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    class Role(models.TextChoices):
        CUSTOMER = "CUSTOMER", "Customer"
        FREELANCER = "FREELANCER", "Freelancer"

    role = models.CharField(max_length=20, choices=Role.choices, default=Role.CUSTOMER)
    bio = models.TextField(blank=True)
    skills = models.CharField(max_length=500, blank=True)
    avatar_url = models.URLField(blank=True)
    location = models.CharField(max_length=120, blank=True)

    @property
    def display_name(self):
        name = f"{self.first_name} {self.last_name}".strip()
        return name or self.username
