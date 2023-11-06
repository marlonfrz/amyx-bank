from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('create_account/', views.bank_account_create_view, name='create_account'),
    path('edit/account/<int:pk>/', views.edit_bank_account, name='edit_account'),
    path('edit/card/<int:pk>/', views.card_edit, name='card_edit'),
    path('card/create', views.card_create, name='card_create'),
]
