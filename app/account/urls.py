from django.urls import path
from django.utils.translation import gettext_lazy as _

from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path(_("accounts/"), views.accounts, name="accounts"),
    path(_("account_create_success/"), views.account_create_success, name="account_create_success"),
    path(_("edit/password/"), views.change_password, name="change_password"),
    path(_("account_detail/<int:id>/"), views.account_detail, name="account_detail"),
    path(_("create_account/"), views.bank_account_create_view, name="create_account"),
    path(_("edit/account/<int:id>/"), views.edit_bank_account, name="edit_account"),
]
