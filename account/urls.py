from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('new_bank_account/', views.bank_account_create_view, name='new_account'),
    path('edit/', views.edit_account, name='edit_account'),
    path('edit/card/', views.edit_card, name='edit_card'),
    path('edit/profile/', views.edit_profile, name='edit_profile'),
    path('account_create_success/', views.account_create_success, name='account_create_success'),
    path('card_detail/', views.card_create_view, name='card_detail'),
]

