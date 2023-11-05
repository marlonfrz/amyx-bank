from django import forms
from .models import Transaction

class TransactionForm(forms.ModelForm):
    agent = forms.CharField(max_length=20)
    concept = forms.CharField(max_length=250)
    amount = forms.DecimalField(max_digits=10, decimal_places=2)
    class Meta:
        model = Transaction
        fields = ['agent', 'concept', 'amount', 'kind']