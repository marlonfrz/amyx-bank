from rest_framework import generics
from account.models import BankAccount
from django.shortcuts import get_object_or_404
from amyx_bank.models import Profile
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated

from account.api.serializers import BankAccountSerializer

class BankAccountListView(generics.ListAPIView):
    serializer_class = BankAccountSerializer
#    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']
    
    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return BankAccount.objects.filter(profile=profile)

class BankAccountDetailView(generics.RetrieveAPIView):
    serializer_class = BankAccountSerializer
#    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        return BankAccount.objects.filter(profile=profile)
