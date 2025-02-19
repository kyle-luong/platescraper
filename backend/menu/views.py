from django.shortcuts import get_object_or_404
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Menu, MenuPeriod, FoodItem
from datetime import date
from django_ratelimit.decorators import ratelimit
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import permission_classes

@api_view(["GET"])
@permission_classes([IsAuthenticated])
@ratelimit(key="ip", rate="10/m", block=True)  # Limit: 10 requests per minute per IP
def get_menu(request, menu_date=None, menu_period=None):
    if not menu_date:
        menu_date = date.today()

    menu = get_object_or_404(Menu, date=menu_date)

    stations_data = {}

    for food_item in FoodItem.objects.filter(menu_period__menu=menu):
        station = food_item.station
        period_name = food_item.menu_period.period_name

        if station.station_id not in stations_data:
            stations_data[station.station_id] = {
                "station_id": station.station_id,
                "station_name": station.station_name,
                "meals": {}
            }

        if period_name not in stations_data[station.station_id]["meals"]:
            stations_data[station.station_id]["meals"][period_name] = []

        stations_data[station.station_id]["meals"][period_name].append(food_item.name)

    return Response({
        "date": str(menu.date),
        "stations": list(stations_data.values())
    })