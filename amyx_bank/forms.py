from django import forms
from django.forms import PasswordInput, TextInput


class LoginForm(forms.Form):
    username = forms.CharField(widget=TextInput())
    password = forms.CharField(widget=PasswordInput())
