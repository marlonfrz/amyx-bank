from django.urls import path

from . import views

urlpatterns = [
    path('', views.transactions, name='transactions'),
    path('buy/', views.buy, name='buy'),
    path('transfer/', views.transfer, name='transfer'),
    path('commissions/', views.commissions, name='commissions'),
]
