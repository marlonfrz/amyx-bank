from django import forms

from .models import Card


class CardCreateForm(forms.ModelForm):
    destined_account = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Card\'s account'}))
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:
        model = Card
        fields = ['card_name']


class CardEditForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_name']
