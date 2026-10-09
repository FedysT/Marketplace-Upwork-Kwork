from django import forms
from .models import Order

class OrderStatusForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["status"]
        widgets = {"status": forms.Select(attrs={"class": "form-select"})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["status"].choices = [
            (Order.Status.ACCEPTED, "Accepted"),
            (Order.Status.IN_PROGRESS, "In progress"),
            (Order.Status.COMPLETED, "Completed"),
            (Order.Status.CANCELLED, "Cancelled"),
        ]
