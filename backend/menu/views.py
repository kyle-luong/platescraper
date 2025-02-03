from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Menu, MenuPeriod, FoodItem
from datetime import date

@api_view(["GET"])
def get_menu(request, menu_date=None, menu_period=None):
    # Default to today's menu
    if not menu_date:
        menu_date = date.today()

    menu = get_object_or_404(Menu, date=menu_date)

    if menu_period:
        menu_period = get_object_or_404(MenuPeriod, menu=menu, period_name=menu_period)
        food_items = FoodItem.objects.filter(menu_period=menu_period).values_list("name", flat=True)
        return Response({
            "date": str(menu_date),
            "period": menu_period.period_name,
            "items": list(food_items)
        })
    
    menu_data = {}
    for menu_period in menu.menu_periods.all():
        food_items = FoodItem.objects.filter(menu_period=menu_period).values_list("name", flat=True)
        menu_data[menu_period.period_name] = list(food_items)

    return Response({
        "date": str(menu.date),
        "menu": menu_data
    })
