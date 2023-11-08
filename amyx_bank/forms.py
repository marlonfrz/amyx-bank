from django import forms
from django.forms import PasswordInput, TextInput

from account.models import Profile

from .models import BankAccount


class LoginForm(forms.Form):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())


class AccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_name']


class AccountEditForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_name']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['avatar', 'date_of_birth']