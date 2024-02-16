from django.urls import include, path
from rest_framework import routers

from account.api import views as account_view
from card.api import views as card_view
from payment.api import views as payment_view

router = routers.DefaultRouter()
router.register('accounts', account_view.BankAccountViewSet)
router.register('cards', card_view.CardViewSet)
router.register('transactions', payment_view.TransactionViewSet)

urlpatterns = [
    path('', include(router.urls)),
]
