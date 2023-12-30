from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

urlpatterns = [
    path("prueba/", views.prueba, name="prueba"),
    path('', views.payment, name='payments'),
    path(_('payment_success/'), views.payment_success, name='payment_success'),
    path(_('payroll/'), views.payroll, name='payroll'),
    path(_('movements/'), views.movements, name='movements'),
    path(_('payment_detail/<int:id>'), views.payment_detail, name='payment_detail'),
    path(_('trasaction_detail/<int:id>'), views.transaction_detail, name='transaction_detail'),
    path(_('trasaction_detail/<int:id>/pdf/'), views.transaction_pdf, name='transaction_pdf'),
    path(_('payment_detail/<int:id>/pdf/'), views.payment_pdf, name='payment_pdf'),
]
