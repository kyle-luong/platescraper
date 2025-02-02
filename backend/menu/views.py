from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Menu
from datetime import date

@api_view(["GET"])
def get_menu(request, menu_date=None, meal_type=None):
    # Default to today's menu
    if not menu_date:
        menu_date = date.today()

    # Fetch the menu for the given date
    menu = get_object_or_404(Menu, date=menu_date)

    # If meal_type is specified, return only that meal's items
    if meal_type:
        meal_data = menu.meals.get(meal_type, [])
        return Response({"date": menu_date, "meal": meal_type, "items": meal_data})

    return Response({"date": menu.date, "meals": menu.meals})
