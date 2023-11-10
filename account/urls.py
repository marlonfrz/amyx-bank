from django.urls import path

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("accounts/", views.accounts, name="accounts"),
    path("account_create_success/", views.account_create_success, name="account_create_success"),
    path("edit/password/", views.change_password, name="change_password"),
    path('account_detail/<int:id>', views.account_detail, name='account_detail'),
    path("create_account/", views.bank_account_create_view, name="create_account"),
    path("edit/account/<int:id>/", views.edit_bank_account, name="edit_account"),
    #   path('account_detail/<int:id>', views.account_detail_view, name='account_detail'),
]
