from django.urls import path

from . import views

urlpatterns = [
    path('', views.dashboard, name='dashboard'),
    path('accounts/', views.accounts, name='accounts'),
    path('edit/profile/', views.edit_profile, name='edit_profile'),
    path('edit/user_info/', views.edit_user_information, name='edit_user_info'),
    path('account_create_success/', views.account_create_success, name='account_create_success'),
    path('edit/password/', views.change_password, name='change_password'),
#   path('account_detail/<int:id>', views.account_detail_view, name='account_detail'),
]
