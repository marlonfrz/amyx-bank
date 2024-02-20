from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

import operator
from django.db.models import Q
from functools import reduce

from account.models import BankAccount
from amyx_bank.models import Profile
from payment.api.serializers import TransactionSerializer
from payment.models import Transaction
from rest_framework.response import Response


class TransactionViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def list(self, request):
        accounts = BankAccount.objects.filter(
            profile=get_object_or_404(Profile, user=self.request.user)
        )
        queryset = Transaction.objects.filter(
            reduce(
                operator.and_,
                (Q(account__icontains=acc.account_code) for acc in accounts),
            )
        ) | Transaction.objects.filter(
            reduce(
                operator.and_,
                (Q(agent__icontains=acc.account_code) for acc in accounts),
            )
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(Transaction, id=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
