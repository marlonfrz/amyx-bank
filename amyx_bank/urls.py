from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("login/", views.user_login, name="login"),
    path("logout/", views.logout, name="logout"),
    path("register/", views.register, name="register"),
    path("create_account/", views.bank_account_create_view, name="create_account"),
    path("edit/account/<int:id>/", views.edit_bank_account, name="edit_account"),
    path("create_card/", views.card_create, name="create_card"),
    path("edit/card/<int:id>/", views.card_edit, name="card_edit"),
    path("card_detail/", views.card_detail, name="card_detail"),
]
