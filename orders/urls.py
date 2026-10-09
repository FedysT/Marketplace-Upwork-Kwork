from django.urls import path
from .views import cancel_order, create_order, order_detail, order_list

urlpatterns = [
    path("", order_list, name="orders"),
    path("create/<int:service_id>/", create_order, name="create_order"),
    path("<int:pk>/", order_detail, name="order_detail"),
    path("<int:pk>/cancel/", cancel_order, name="cancel_order"),
]
