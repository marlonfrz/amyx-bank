from rest_framework import serializers
from payment.models import Transaction

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = [ 'agent', 'account', 'amount', 'timestamp', 'kind' ,]
