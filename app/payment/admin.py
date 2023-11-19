from django.contrib import admin

# Register your models here.
from .models import Transaction, Payment



@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['agent', 'account', 'concept', 'amount', 'kind', 'timestamp']

@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ['business', 'card', 'amount', 'kind', 'timestamp']
