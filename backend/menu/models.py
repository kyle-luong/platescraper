from django.db import models

class Menu(models.Model):
    date = models.DateField(unique=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Menu for {self.date}"

class Station(models.Model):
    station_id = models.CharField(max_length=20, unique=True)
    station_name = models.CharField(max_length=255)

    def __str__(self):
        return self.station_name

class MenuPeriod(models.Model):
    PERIOD_CHOICES = [
        ("Breakfast", "Breakfast"),
        ("Brunch", "Brunch"),
        ("Lunch", "Lunch"),
        ("Dinner", "Dinner"),
        ("All Day", "All Day"),
    ]

    menu = models.ForeignKey(Menu, on_delete=models.CASCADE, related_name="menu_periods")
    period_name = models.CharField(max_length=20, choices=PERIOD_CHOICES)
    period_id = models.CharField(max_length=10)

    def __str__(self):
        return f"{self.period_name} on {self.menu.date}"

class FoodItem(models.Model):
    menu_period = models.ForeignKey(MenuPeriod, on_delete=models.CASCADE, related_name="food_items")
    station = models.ForeignKey(Station, on_delete=models.CASCADE, related_name="food_items")
    name = models.CharField(max_length=255)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.name} ({self.menu_period.period_name} at {self.station.station_name} on {self.menu_period.menu.date})"
