from django.urls import path

from . import views

urlpatterns = [
    path('', views.payment, name='payments'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payroll/', views.payroll, name='payroll'),
    path('movements/', views.movements, name='movements'),
    path('payment_detail/<int:id>', views.payment_detail, name='payment_detail'),
    path('trasaction_detail/<int:id>', views.transaction_detail, name='transaction_detail'),
    path('trasaction_detail/<int:id>/pdf/',views.transaction_pdf, name='transaction_pdf'),
    path('payment_detail/<int:id>/pdf/',views.payment_pdf, name='payment_pdf'),

]
