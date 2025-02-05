import requests
from datetime import datetime
from menu.models import Menu, Station, MenuPeriod, FoodItem

PERIOD_MAPPING = {
    "1421": "Breakfast",
    "1422": "Lunch",
    "1423": "Dinner",
    "1424": "Brunch",
    "2181": "All Day",
}

def fetch_menu_from_api(api_date):
    url = f"https://virginia.campusdish.com/api/menu/GetMenus?locationId=695&storeIds=&mode=Daily&date={api_date}&fulfillmentMethod="
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch menu for {api_date}")
        return None

    return response.json()

def get_or_create_menu(db_date):
    menu, _ = Menu.objects.get_or_create(date=db_date)
    return menu

def get_or_create_station(station_id, station_name):
    station, _ = Station.objects.get_or_create(station_id=station_id, defaults={"station_name": station_name})
    return station

def get_or_create_menu_period(menu, period_name, period_id):
    menu_period, _ = MenuPeriod.objects.get_or_create(
        menu=menu, period_name=period_name, period_id=period_id
    )
    return menu_period

def get_or_create_food_item(menu_period, station, name, description):
    FoodItem.objects.get_or_create(
        menu_period=menu_period,
        station=station,
        name=name,
        description=description
    )

def sync_menu_data():
    api_date = datetime.today().strftime("%m/%d/%Y")
    db_date = datetime.today().strftime("%Y-%m-%d")

    menu_data = fetch_menu_from_api(api_date)
    if not menu_data:
        return
    
    menu_stations = menu_data.get("Menu", {}).get("MenuStations", [])
    menu_products = menu_data.get("Menu", {}).get("MenuProducts", [])

    menu = get_or_create_menu(db_date)

    # Process stations
    station_map = {}
    for station in menu_stations:
        station_id = station.get("StationId")
        station_name = station.get("Name", "Unnamed Station")
        if station_id:
            station_map[station_id] = get_or_create_station(station_id, station_name)

    period_meals = {}

    # Process food items
    for product in menu_products:
        period_id = product.get("PeriodId")
        station_id = product.get("StationId")

        if not period_id or not station_id or station_id not in station_map:
            continue

        station = station_map[station_id]
        product_info = product.get("Product", {})
        product_name = product_info.get("MarketingName", "Unnamed Product")
        description = product_info.get("ShortDescription", "No description available")

        if period_id not in period_meals:
            period_meals[period_id] = []

        period_meals[period_id].append((station, product_name, description))

    for period_id, meals in period_meals.items():
        period_name = PERIOD_MAPPING.get(period_id, "Unknown")

        if period_name == "Unknown":
            continue

        menu_period = get_or_create_menu_period(menu, period_name, period_id)

        for station, name, desc in meals:
            get_or_create_food_item(menu_period, station, name, desc)

    print(f"Menu for {db_date} stored successfully!")
