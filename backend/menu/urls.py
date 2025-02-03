from django.urls import path
from .views import get_menu

urlpatterns = [
    path("menu/", get_menu),  # Fetch today's menu
    path("menu/<str:menu_date>/", get_menu),  # Fetch menu for a specific date
    path("menu/<str:menu_date>/<str:meal_period>/", get_menu),  # Fetch menu for a specific meal type
]
