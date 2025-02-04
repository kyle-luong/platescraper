import requests
from datetime import datetime
from menu.models import Menu, MenuPeriod, FoodItem

def fetch_menu_from_api(api_date):
    url = f"https://virginia.campusdish.com/api/menu/GetMenus?locationId=695&storeIds=&mode=Daily&date={api_date}&fulfillmentMethod="
    
    response = requests.get(url)
    if response.status_code != 200:
        print(f"Failed to fetch menu for {api_date}")
        return None

    return response.json()

def get_active_menu_periods(menu_data):
    active_periods = {}

    menu_periods = menu_data.get("Menu", {}).get("MenuPeriods", [])
    for period in menu_periods:
        if period.get("IsActive", False):  # Only include active periods
            period_name = period.get("Name", "Unknown")
            period_id = period.get("PeriodId", "")
            active_periods[period_name] = period_id

    return active_periods


def get_or_create_menu(db_date):
    menu, created = Menu.objects.get_or_create(date=db_date)
    return menu

def get_or_create_menu_period(menu, period_name, period_id):
    menu_period, created = MenuPeriod.objects.get_or_create(
        menu=menu, period_name=period_name, period_id=period_id
    )
    return menu_period

def get_or_create_food_item(menu_period, name, description):
    FoodItem.objects.get_or_create(
        menu_period=menu_period,
        name=name,
        description=description
    )

def sync_menu_data():
    api_date = datetime.today().strftime("%m/%d/%Y")
    db_date = datetime.today().strftime("%Y-%m-%d")

    # Fetch menu data from API
    menu_data = fetch_menu_from_api(api_date)
    if not menu_data:
        return

    # Get available meal periods from API response
    menu_periods = get_active_menu_periods(menu_data)
    if not menu_periods:
        print(f"No menu periods available for {db_date}")
        return

    menu = get_or_create_menu(db_date)

    for period_name, period_id in menu_periods.items():
        print(f"Processing {period_name} (ID: {period_id})...")

        menu_products = menu_data.get("Menu", {}).get("MenuProducts", [])

        meal_period = get_or_create_menu_period(menu, period_name, period_id)

        for product in menu_products:
            if product.get("PeriodId") != period_id:
                continue

            product_info = product.get("Product", {})
            product_name = product_info.get("MarketingName", "Unnamed Product")
            description = product_info.get("ShortDescription", "No description available")
            get_or_create_food_item(meal_period, product_name, description)

    print(f"Menu for {db_date} stored successfully!")