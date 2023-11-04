from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views..logologin, name='login'),
    path('logout/', views.logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('register/', views.register, name='register'),
    path('new_bank_account/', views.bank_account_create_view, name='new_account'),
    path('edit_card/', views.edit_card, name='edit_card'),
    path('edit_account/', views.edit_account, name='edit_account'),
    path('account_create_success/', views.account_create_success, name='account_create_success'),
    #    path('', include('django.contrib.auth.urls')),
]
