from django.db import models

class Menu(models.Model):
    date = models.DateField(unique=True)
    items = models.JSONField()
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Menu for {self.date}"
