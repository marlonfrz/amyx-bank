from django.contrib.auth import views as auth_views
from django.urls import include, path

from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('new_bank_account/', views.bank_account_create_view, name='new_account'),
    path('account_create_success/', views.account_create_success, name='account_create_success'),
    path('', include('django.contrib.auth.urls')),
]
