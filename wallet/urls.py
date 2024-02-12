from django.urls import path
from .api import wallet

urlpatterns = [
    path('<str:user_id>/info', wallet.get_wallets_info, name='get_wallets_info'),
    path('<str:user_id>/transfer', wallet.transfer_money, name='transfer_money'),
]