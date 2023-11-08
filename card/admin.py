from django.contrib import admin

from .models import Card


@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ['card_name', 'card_validation_code', 'card_account_code', 'account', 'status']
