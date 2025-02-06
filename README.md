# platescraper
### Menu to iOS app and widget
A Django-based API that fetches menu data and provides structured endpoints for integration with an iOS app and widget.

---

### Clone the repository:
```sh
git clone https://github.com/kyle-luong/platescraper.git
```

### Create and activate virtual environment
**Windows:**
```
py -m venv .venv
.venv\Scripts\activate
```
**Unix/macOS**
```
python3 -m venv .venv
source .venv/bin/activate
```

### Install dependencies
```
pip install -r requirements.txt
```

### Set Up Django Database
```
cd backend
python manage.py makemigrations menu
python manage.py migrate
```

### Run the server
```
cd backend
python manage.py runserver
```
---
### API Endpoints
Method	| Endpoint	| Description
--- | --- | ---
GET	| /api/menu/ | Get today's menu
GET	| /api/menu/YYYY-MM-DD/ | Get menu for a specific date
GET	| /api/menu/YYYY-MM-DD/meal-type/ | Get menu for a specific meal period

---
### Manually sync menu data
```
cd backend
python manage.py shell
>>> from menu.sync_menu import sync_menu_data
>>> sync_menu_data()
```
- Planned Feature: Schedule daily automatic menu syncing.

---
