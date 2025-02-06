import requests
from datetime import datetime
from menu.models import Menu, Station, MenuPeriod, FoodItem

PERIOD_MAPPING = {
    "1421": "Breakfast",
    "1422": "Brunch",
    "1423": "Lunch",
    "1424": "Dinner",
    "2181": "All Day",
}

def fetch_menu_from_api(api_date, period_id):
    url = f"https://virginia.campusdish.com/api/menu/GetMenus?locationId=695&mode=Daily&date={api_date}&periodId={period_id}"
    
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

    menu = get_or_create_menu(db_date)

    for period_id, period_name in PERIOD_MAPPING.items():
        menu_data = fetch_menu_from_api(api_date, period_id)
        if not menu_data: continue

        menu_stations = menu_data.get("Menu", {}).get("MenuStations", [])
        menu_products = menu_data.get("Menu", {}).get("MenuProducts", [])

        menu_period = get_or_create_menu_period(menu, period_name, period_id)

        for station in menu_stations:
            get_or_create_station(station["StationId"], station["Name"])

        for product in menu_products:
            station_id = product.get("StationId")
            product_info = product.get("Product", {})
            product_name = product_info.get("MarketingName", "Unnamed Product")
            description = product_info.get("ShortDescription", "No description available")

            station = get_or_create_station(station_id, "Unknown Station")
            get_or_create_food_item(menu_period, station, product_name, description)

        print(f"Processed {period_name}")

    print(f"Menu for {db_date} stored successfully!")