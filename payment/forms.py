from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['agent', 'concept', 'amount', 'kind']

class PaymentForm(forms.ModelForm):
    business = forms.CharField(max_length=100)
    ccc = forms.CharField(max_length=7)
    pin = forms.CharField(max_length=3)
    class Meta:
        model = Transaction
        fields = ['amount']