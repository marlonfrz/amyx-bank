from account.models import BankAccount
from django import forms
from payment.models import Card, Payment, Transaction


class TransactionForm(forms.ModelForm):
    sender = forms.ModelChoiceField(
        queryset=BankAccount.objects.none(), to_field_name="account_code"
    )
    cac = forms.CharField(
        max_length=7,
        widget=forms.TextInput(
            attrs={'id': 'cac', 'pattern': '[aA][0-9]-[0-9]{4}', 'placeholder': 'A9-0000'}
        ),
    )

    class Meta:
        model = Transaction
        fields = ['concept', 'amount']
        widgets = {
            'concept': forms.TextInput(attrs={'id': 'concept'}),
            'amount': forms.NumberInput(attrs={'id': 'amount', 'style': 'appereance: none'}),
        }

    def __init__(self, profile=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['sender'].queryset = BankAccount.objects.filter(profile=profile).exclude(
            status=BankAccount.Status.CANCELLED
        )

class PaymentForm(forms.ModelForm):
    business = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id': 'business'}))
    ccc = forms.ModelChoiceField(Card.objects.none(), to_field_name="card_code")
    pin = forms.CharField(
        max_length=3,
        widget=forms.TextInput(
            attrs={'id': 'pin', 'pattern': '[a-zA-Z-0-9]{3}', 'placeholder': 'PPP'}
        ),
    )

    class Meta:
        model = Payment
        fields = ['amount']
        widgets = {
            'amount': forms.NumberInput(attrs={'id': 'amount', 'style': 'appereance: none'}),
        }

    def __init__(self, accounts=[], *args, **kwargs):
        super().__init__(*args, **kwargs)
        if accounts:
            self.fields['ccc'].queryset = Card.objects.filter(account=accounts[0])
            cards = accounts[0].cards.exclude(status=Card.Status.CANCELLED)
            for account in accounts:
                cards = cards | account.cards.exclude(status=Card.Status.CANCELLED)
            self.fields['ccc'].queryset = cards
        else:
            self.fields['ccc'].queryset = Card.objects.none()
