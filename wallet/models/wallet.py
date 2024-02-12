from django.db import models
from django.contrib.auth.models import User

class Wallet(models.Model):
    class CurrencyEnum(models.TextChoices):
        RUB = 'RUB', 'RUB'
        USD = 'USD', 'USD'
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    currency = models.CharField(max_length=3, choices=CurrencyEnum.choices)
    balance = models.DecimalField(max_digits=10, decimal_places=2)
    # Add more fields as needed

    def __str__(self):
        return f"{self.user.username}'s {self.currency} Wallet"
