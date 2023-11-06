from django.urls import include, path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('register/', views.register, name='register'),
    path('edit/account/', views.edit_bank_account, name='edit_account'),
]
