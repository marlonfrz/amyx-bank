from django.shortcuts import get_object_or_404
from rest_framework import generics, viewsets
from rest_framework.authentication import BasicAuthentication, SessionAuthentication
from rest_framework.permissions import IsAuthenticated

from account.api.serializers import BankAccountSerializer
from account.models import BankAccount
from amyx_bank.models import Profile
from rest_framework.response import Response


class BankAccountViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BankAccount.objects.all()
    serializer_class = BankAccountSerializer
    authentication_classes = [SessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    http_method_names = ["get"]

    def list(self, request):
        queryset = BankAccount.objects.filter(
            profile=get_object_or_404(Profile, user=self.request.user)
        )
        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        queryset = get_object_or_404(BankAccount, id=pk)
        serializer = self.get_serializer(queryset)
        return Response(serializer.data)
