from django import forms
from payment.models import Transaction, Payment

class TransactionForm(forms.ModelForm):
    sender = forms.CharField(max_length=7, widget=forms.TextInput(attrs={'id': 'sender', 'pattern': '[aA][0-9]-[0-9]{4}', 'placeholder': 'A5-0000'}))
    cac = forms.CharField(max_length=7, widget=forms.TextInput(attrs={'id': 'cac', 'pattern': '[aA][0-9]-[0-9]{4}', 'placeholder': 'A9-0000'}))

    class Meta:
        model = Transaction
        fields = ['concept', 'amount']
        widgets = {
            'concept': forms.TextInput(attrs={'id': 'concept'}),
            'amount': forms.TextInput(attrs={'id': 'amount'}),
        }

class PaymentForm(forms.ModelForm):
    business = forms.CharField(max_length=100, widget=forms.TextInput(attrs={'id': 'business'}))
    ccc = forms.CharField(max_length=7, widget=forms.TextInput(attrs={'id': 'ccc', 'pattern': '[cC][0-9]-[0-9]{4}', 'placeholder': 'C9-0000'}))
    pin = forms.CharField(max_length=3, widget=forms.TextInput(attrs={'id': 'pin', 'pattern': '[a-zA-Z-0-9]{4}', 'placeholder': 'C9-0000'}))
    class Meta:
        model = Payment
        fields = ['amount']
        widgets = {
            'amount': forms.TextInput(attrs={'id': 'amount'}),
        }
