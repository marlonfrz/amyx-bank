from django.urls import path

from . import views

urlpatterns = [
    path('', views.payment, name='payments'),                                                   
    path('payment_success/', views.payment_success, name='payment_success'),                    #Falta por hacer las
    path('payroll/', views.payroll, name='payroll'),
    path('incoming/', views.incoming_transactions, name='incoming'),
    path('movements/', views.movements, name='movements'),
    path('payment_detail/<int:id>', views.payment_detail, name='payment_detail'),
    path('trasaction_detail/<int:id>', views.transaction_detail, name='transaction_detail'),
]
