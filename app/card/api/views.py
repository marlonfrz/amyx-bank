from account.models import BankAccount
from amyx_bank.models import Profile
from card.api.serializers import CardSerializer
from card.models import Card
from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# Card serializer


class CardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Card.objects.all()
    serializer_class = CardSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def list(self, request):
        queryset = Card.objects.filter(account__profile__user=self.request.user)
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(Card, id=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
