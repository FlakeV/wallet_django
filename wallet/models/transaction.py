from django.db import models
from django.core.exceptions import ValidationError
from .wallet import Wallet


class Transaction(models.Model):
    id = models.BigAutoField(primary_key=True)
    sender_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='sender')
    recipient_wallet = models.ForeignKey(Wallet, on_delete=models.CASCADE, related_name='recipient')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sender_wallet.user.username} to {self.recipient_wallet.user.username} withdraw"

    def clean(self):
        if self.sender_wallet.currency != self.recipient_wallet.currency:
            raise ValidationError("Sender and recipient wallets must have the same currency")

        if self.sender_wallet.balance < self.amount:
            raise ValidationError("Not enough money in the sender wallet")
