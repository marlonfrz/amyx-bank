from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('edit/card/', views.edit_card, name='edit_card'),
    path('edit/profile/', views.edit_profile, name='edit_profile'),
    path('account_create_success/', views.account_create_success, name='account_create_success'),
    path('card_detail/', views.card_create_view, name='card_detail'),
    path('edit/password/', views.change_password, name='change_password'),
    path('account_detail/', views.account_create_view, name='account_detail'),
]
