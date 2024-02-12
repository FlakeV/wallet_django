import logging

from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from wallet.models import Wallet
from wallet.logic.wallet import transfer_money_tool, get_wallet_or_none
from wallet.serializers import WalletSerializer


logger = logging.getLogger('wallet')

@api_view(['GET'])
def get_wallets_info(request, user_id):
    wallets = Wallet.objects.filter(user_id=user_id).all()
    data = []
    for wallet in wallets:
        data.append({
            'id': wallet.id,
            'balance': wallet.balance,
        })
    data = WalletSerializer(data, many=True).data
    logger.info(f'Get wallets info by user {user_id}')
    return Response(data, status=status.HTTP_200_OK)


@api_view(['POST'])
def transfer_money(request, user_id):
    sender_wallet_id = request.data.get('sender_wallet_id')
    recipient_wallet_id = request.data.get('recipient_wallet_id')
    amount = request.data.get('amount')

    # Проверка наличия кошельков и достаточного баланса у отправителя
    sender_wallet = get_wallet_or_none(sender_wallet_id)
    recipient_wallet = get_wallet_or_none(recipient_wallet_id)
    # assert False, f'{sender_wallet.balance} {recipient_wallet.balance}'
    if not sender_wallet or not recipient_wallet:
        logger.info(f'Sender or recipient wallet not found')
        return Response({'message': 'Sender or recipient wallet not found'}, status=status.HTTP_400_BAD_REQUEST)
    if sender_wallet.user.id != int(user_id):
        logger.info(f'User {user_id} doesn\'t have access to wallet {sender_wallet.id}')
        return Response({'message': 'You don\'t have access to this wallet'}, status=status.HTTP_400_BAD_REQUEST)
    if sender_wallet.balance < amount:
        logger.info(f'There is not enough balance on the wallet {sender_wallet.id}')
        return Response({'message': 'Not enough money in the sender wallet'}, status=status.HTTP_400_BAD_REQUEST)
    if sender_wallet.currency != recipient_wallet.currency:
        logger.info(
            f'Sender and recipient wallets must have the same currency sent {sender_wallet.currency} received {recipient_wallet.currency}'
        )
        return Response({'message': 'Sender and recipient wallets must have the same currency'}, status=status.HTTP_400_BAD_REQUEST)

    # Если все проверки прошли успешно, производим перевод
    transfer_money_tool(sender_wallet, recipient_wallet, amount)
    logger.info(f'Money transferred from wallet {sender_wallet.id} to wallet {recipient_wallet.id} by user {user_id}')
    # Возвращаем ответ об успешном выполнении
    return Response({'message': 'Money transferred successfully'}, status=status.HTTP_200_OK)