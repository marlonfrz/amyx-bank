from django.urls import path

from . import views

app_name = "payments"

urlpatterns = [
    path('', views.payment, name='payments'),
    path('payment_success/', views.payment_success, name='payment_success'),
    path('payroll/', views.payroll, name='payroll'),
    path('payments/all/', views.payment_list, name='payment_list'),
    path('transactions/all/', views.transaction_list, name='transaction_list'),
    path('payment_detail/<int:id>', views.payment_detail, name='payment_detail'),
    path('trasaction_detail/<int:id>', views.transaction_detail, name='transaction_detail'),
    path('trasaction_detail/<int:transaction_id>/pdf/', views.transaction_pdf, name='transaction_pdf'),
    path('payment_detail/<int:payment_id>/pdf/', views.payment_pdf, name='payment_pdf'),
    path('export_movements/csv', views.export_csv, name='export_movements'),
]
