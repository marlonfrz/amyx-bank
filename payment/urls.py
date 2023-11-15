from django.urls import path

from . import views

urlpatterns = [
    path('', views.payment, name='payments'),                                                   #Falta por hacer las
    path('payment_success/', views.payment_success, name='payment_success'),                    #Falta por hacer las
    path('payroll/', views.payroll, name='payroll'),
    path('incoming/', views.incoming_transactions, name='incoming')
]
