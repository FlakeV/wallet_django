from rest_framework import serializers

class WalletSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    balance = serializers.DecimalField(max_digits=10, decimal_places=2)


class TransactionSerializer(serializers.Serializer):
    id = serializers.IntegerField()
    amount = serializers.DecimalField(max_digits=10, decimal_places=2)
    date = serializers.DateTimeField()