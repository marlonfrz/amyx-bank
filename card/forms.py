from django import forms

from account.models import BankAccount

from .models import Card


class CardCreateForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    accounts = forms.ModelChoiceField(queryset=BankAccount.objects.none())

    class Meta:
        model = Card
        fields = ['card_name']

    def __init__(self, profile=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['accounts'].queryset = BankAccount.objects.filter(profile=profile)


class CardEditForm(forms.ModelForm):
    class Meta:
        model = Card
        fields = ['card_name']
