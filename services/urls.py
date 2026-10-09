from django.urls import path
from .views import category_list, create_service, edit_service, home, my_services, service_detail

urlpatterns = [
    path("", home, name="home"),
    path("categories/", category_list, name="categories"),
    path("create/", create_service, name="create_service"),
    path("mine/", my_services, name="my_services"),
    path("<int:pk>/", service_detail, name="service_detail"),
    path("<int:pk>/edit/", edit_service, name="edit_service"),
]
