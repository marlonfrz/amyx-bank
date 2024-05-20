from django import forms
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth.models import User

from account.models import BankAccount


class ChangePasswordForm(PasswordChangeForm):
    class Meta:
        model = User
        fields = ['old_password', 'new_password1', 'new_password2']


class AccountForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput, help_text="Type your password to create a new account")

    class Meta:
        model = BankAccount
        fields = ['account_name']


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_name', 'status']
