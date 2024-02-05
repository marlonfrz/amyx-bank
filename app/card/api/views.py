from rest_framework import generics
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from account.models import BankAccount
from amyx_bank.models import Profile
from card.models import Card
from card.api.serializers import CardSerializer
from django.shortcuts import get_object_or_404

# Card serializer

class CardListView(generics.ListAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        accounts = BankAccount.objects.filter(profile=profile)
        cards = accounts[0].cards.all()
        for account in accounts[1:]:
            cards = cards | account.cards.all()
        return cards
    
class CardDetailView(generics.RetrieveAPIView):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get']

    def get_queryset(self):
        profile = get_object_or_404(Profile, user=self.request.user)
        accounts = BankAccount.objects.filter(profile=profile)
        cards = accounts[0].cards.all()
        for account in accounts[1:]:
            cards = cards | account.cards.all()
        return cards
