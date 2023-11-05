from django import forms
from django.forms import PasswordInput, TextInput
from .models import BankAccount


class LoginForm(forms.Form):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_name']
