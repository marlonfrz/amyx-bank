from django import forms
from django.contrib.auth.models import User
from django.forms import PasswordInput, TextInput

from .models import BankAccount, Profile


class LoginForm(forms.Form):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())

    class Meta:
        widgets = {
            'username': TextInput(
                attrs={
                    'class': "form-control bg-white border-left-0 border-md",
                    'id': "firstName",
                    'placeholder': "Name",
                    'type': "text",
                }
            ),
            'password': PasswordInput(
                attrs={
                    'class': "form-control bg-white border-left-0 border-md",
                    'id': "password",
                    'placeholder': "Password",
                    'type': "password",
                }
            ),
        }


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


class UserEditForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

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
