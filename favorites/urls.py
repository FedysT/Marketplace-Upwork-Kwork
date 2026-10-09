from django.urls import path
from .views import favorite_list, toggle_favorite

urlpatterns = [
    path("", favorite_list, name="favorites"),
    path("toggle/<int:service_id>/", toggle_favorite, name="toggle_favorite"),
]
