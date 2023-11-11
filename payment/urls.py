from django.urls import path

from . import views

urlpatterns = [
    path('', views.payment, name='payments'),             #Falta por hacer las
    path('transactions/', views.transactions, name='transactions'),           #Falta por hacer las plantillas
    path('buy/', views.buy, name='buy'),                         #Falta por hacer las plantillas
    path('transfer/', views.transfer, name='transfer'),          #Falta por hacer las plantillas
    path('commissions/', views.commissions, name='commissions'), #Falta por hacer las plantillas
    path('payment_success/', views.payment_success, name='payment_success'),             #Falta por hacer las
]
