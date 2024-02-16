from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from account.api.serializers import BankAccountSerializer
from account.models import BankAccount
from amyx_bank.models import Profile


class BankAccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return BankAccount.objects.filter(profile=profile)
