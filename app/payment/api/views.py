from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from account.models import BankAccount
from amyx_bank.models import Profile
from payment.api.serializers import TransactionSerializer
from payment.models import Transaction


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        accounts = BankAccount.objects.filter(profile=get_object_or_404(Profile, user=self.request.user))
        transactions_accounts = None
        transactions_agents = None
        for account in accounts:
            if transactions_accounts is None:
                transactions_accounts = Transaction.objects.filter(account__icontains=account.account_code)
                transactions_agents = Transaction.objects.filter(agent__icontains=account.account_code)
            else:
                transactions_accounts = transactions_accounts | Transaction.objects.filter(account__icontains=account.account_code)
                transactions_agents = transactions_agents | Transaction.objects.filter(agent__icontains=account.account_code)
        transactions = transactions_agents | transactions_accounts
        return transactions
