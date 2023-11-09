from django import forms

from .models import Card


class CardCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    def __init__(self, accounts=[], *args, **kwargs):
        super(CardCreateForm, self).__init__(*args, **kwargs)
        self.fields['accounts'] = forms.ModelChoiceField(
                queryset=accounts, widget=forms.Select({'id': 'accounts'}))


    class Meta:
        model = Card
        fields = ['card_name']


class CardEditForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_name']
