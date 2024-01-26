from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('transactions/',views.TransactionListView.as_view(), name='transaction_list'),
    path('transactions/<pk>/', views.TransactionDetailView.as_view(), name='transaction_detail'),
]