from django import forms
from django.contrib.auth.models import User
from django.forms import PasswordInput, TextInput
from django.contrib.auth.forms import UserChangeForm

from .models import Profile
from amyx_bank.models import BankAccount


class UserRegistrationForm(forms.ModelForm):
    username = forms.CharField(max_length=20)
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Repeat password', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ["username", "first_name", "last_name", "email"]

    def clean_password2(self):
        cd = self.cleaned_data
        if cd["password"] != cd["password2"]:
            raise forms.ValidationError("Passwords don\'t match")
        return cd["password2"]


class UserEditForm(UserChangeForm):
    class Meta:
        model = User
        fields = ['password', 'email']

    def clean_email(self):
        data = self.cleaned_data['email']
        qs = User.objects.exclude(id=self.instance.id).filter(email=data)
        if qs.exists():
            raise forms.ValidationError(' Email already in use.')
        return data


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['date_of_birth']


def clean_email(self):
    data = self.cleaned_data['email']
    if User.objects.filter(email=data).exists():
        raise forms.ValidationError('Email already in use.')
    return data


class BankAccountForm(forms.ModelForm):
    class Meta:
        model = BankAccount
        fields = ['account_name']