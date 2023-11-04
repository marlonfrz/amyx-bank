from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='dashboard'),
    path('new_bank_account/', views.bank_account_create_view, name='new_account'),
    path('edit/account', views.edit_account, name='edit_account'),
    path('edit/card/', views.edit_card, name='edit_card'),
    path('edit/profile/', views.edit_profile, name='edit_profile'),
    path('account_create_success/', views.account_create_success, name='account_create_success'),
]