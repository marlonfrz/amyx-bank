from django.contrib import admin

from .models import BankAccount, Card

# Register your models here.
admin.site.register(BankAccount)
admin.site.register(Card)
