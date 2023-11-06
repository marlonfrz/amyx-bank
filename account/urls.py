from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('edit/card/', views.edit_card, name='edit_card'),
    path('edit/profile/', views.edit_profile, name='edit_profile'),
    path('edit/user_info/', views.edit_user_information, name='edit_user_info'),
    path('account_create_success/', views.account_create_success, name='account_create_success'),
    path('card_detail/', views.card_create_view, name='card_detail'),
    path('edit/password/', views.change_password, name='change_password'),
#   path('account_detail/<int:id>', views.account_detail_view, name='account_detail'),
]
