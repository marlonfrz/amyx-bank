from rest_framework import serializers

from account.models import BankAccount


class BankAccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankAccount
        fields = ['profile', 'account_name', 'balance', 'account_code', 'status']
