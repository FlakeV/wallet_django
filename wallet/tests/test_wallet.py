from rest_framework.test import APITestCase
from rest_framework import status
from django.urls import reverse
from django.contrib.auth.models import User
from wallet.models import Wallet, Transaction


class WalletAPITest(APITestCase):
    def setUp(self):
        self.sender = User.objects.create(
            username='sender',
            email='test_1@example.com',
            password='password123'
        )
        self.receiver = User.objects.create(
            username='receiver',
            email='test_2@example.com',
            password='password123'
        )
        # Create sender wallet
        self.sender_wallet = Wallet.objects.create(
            user=self.sender,
            currency='RUB',
            balance=10000
        )
        # Create receiver wallet
        self.receiver_wallet = Wallet.objects.create(
            user=self.receiver,
            currency='RUB',
            balance=0
        )

    def test_get_wallets(self):
        url = reverse('get_wallets_info', args=[self.sender.id])
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fund_transfer_success(self):
        url = reverse('transfer_money', args=[self.sender.id])
        data = {
            'sender_wallet_id': self.sender_wallet.id,
            'recipient_wallet_id': self.receiver_wallet.id,
            'amount': 100
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_fund_transfer_fail(self):
        url = reverse('transfer_money', args=[self.sender.id])
        data = {
            'sender_wallet_id': self.sender_wallet.id,
            'recipient_wallet_id': self.receiver_wallet.id,
            'amount': 100000
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('Not enough money in the sender', response.data['message'])

    def test_not_access_to_wallet(self):
        url = reverse('transfer_money', args=[self.receiver.id])
        data = {
            'sender_wallet_id': self.sender_wallet.id,
            'recipient_wallet_id': self.receiver_wallet.id,
            'amount': 100
        }
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn('You don\'t have access to this wallet', response.data['message'])
