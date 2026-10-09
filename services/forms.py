from django import forms
from .models import Service

class ServiceForm(forms.ModelForm):
    class Meta:
        model = Service
        fields = ["title", "category", "description", "price", "delivery_days", "image_url", "is_active"]
        widgets = {
            "title": forms.TextInput(attrs={"class": "form-control", "placeholder": "I will build..."}),
            "category": forms.Select(attrs={"class": "form-select"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 7, "placeholder": "Describe what the customer will get..."}),
            "price": forms.NumberInput(attrs={"class": "form-control", "min": "1", "step": "0.01"}),
            "delivery_days": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "image_url": forms.URLInput(attrs={"class": "form-control", "placeholder": "Optional image URL"}),
            "is_active": forms.CheckboxInput(attrs={"class": "form-check-input"}),
        }
