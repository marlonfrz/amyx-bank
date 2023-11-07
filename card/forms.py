from django import forms

from .models import Card


class CardCreateForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_name']


class CardEditForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_name']
