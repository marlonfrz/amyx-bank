from django.contrib import admin

from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['card_name', 'cvc', 'card_account_code', 'account', 'status']
