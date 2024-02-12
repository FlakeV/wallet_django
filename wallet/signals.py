from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Transaction


@receiver(post_save, sender=Transaction)
def update_wallet_balances(sender, instance, created, **kwargs):
    if created:
        # Обновляем баланс отправителя
        instance.sender_wallet.balance -= instance.amount
        instance.sender_wallet.save()

        # Обновляем баланс получателя
        instance.recipient_wallet.balance += instance.amount
        instance.recipient_wallet.save()
