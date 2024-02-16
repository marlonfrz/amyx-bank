from django.db.models import Q
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated

from account.models import BankAccount
from amyx_bank.models import Profile
from card.models import Card
from payment.api.serializers import TransactionSerializer
from payment.models import Transaction


# @api_view(["GET", "POST"])
class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
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
