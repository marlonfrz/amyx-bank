from account.models import BankAccount
from amyx_bank.models import Profile
from card.api.serializers import CardSerializer
from card.models import Card
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

# Card serializer


class CardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        return Card.objects.filter(account_profile__user=self.request.user)
