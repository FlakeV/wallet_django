from wallet.models import Wallet, Transaction


def _update_wallet_balance(sender_wallet: Wallet, recipient_wallet: Wallet, amount):
    sender_wallet.balance -= amount
    recipient_wallet.balance += amount
    sender_wallet.save()
    recipient_wallet.save()


def transfer_money_tool(sender_wallet: Wallet, recipient_wallet: Wallet, amount):
    _update_wallet_balance(sender_wallet, recipient_wallet, amount)

    # Создаем транзакции
    Transaction.objects.create(
        sender_wallet=sender_wallet,
        recipient_wallet=recipient_wallet,
        amount=amount
    )


def get_wallet_or_none(wallet_id):
    try:
        return Wallet.objects.get(id=wallet_id)
    except Wallet.DoesNotExist:
        return None
