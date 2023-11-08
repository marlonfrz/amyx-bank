from django.contrib import admin

from .models import BankAccount


# Register your models here.
@admin.register(BankAccount)
class BankAccountAdmin(admin.ModelAdmin):
    list_display = ['account_code', 'account_name', 'account_balance', 'status', 'profile']
