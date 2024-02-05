from rest_framework import generics
from payment.models import Transaction
from payment.api.serializers import TransactionSerializer
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from django.shortcuts import get_object_or_404
from account.models import BankAccount
from amyx_bank.models import Profile
from card.models import Card
from django.db.models import Q


class TransactionListView(generics.ListAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        accounts = BankAccount.objects.filter(profile=profile)
        account_codes = [account.account_code for account in accounts]
        transactions_accounts = Transaction.objects.filter(account__in=account_codes)
        transactions_agents = Transaction.objects.filter(agent__in=account_codes)
        transactions = transactions_agents | transactions_accounts
        return transactions

class TransactionDetailView(generics.RetrieveAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        accounts = BankAccount.objects.filter(profile=profile)
        account_codes = [account.account_code for account in accounts]
        transactions_accounts = Transaction.objects.filter(account__in=account_codes)
        transactions_agents = Transaction.objects.filter(agent__in=account_codes)
        transactions = transactions_agents | transactions_accounts
        return transactions
