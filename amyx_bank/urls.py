from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.log_out, name="logout"),
    path("register/", views.register, name="register"),
    path('account_detail/<int:id>', views.account_detail, name='account_detail'),
    path("create_account/", views.bank_account_create_view, name="create_account"),
    path("edit/account/<int:id>/", views.edit_bank_account, name="edit_account"),
    # path('inicio/', views.inicio, name='inicio'),
    # path('detalle/<int:id>/', views.detalle, name='detalle'),
]
