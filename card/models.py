from django.db import models
from django.urls import reverse

from amyx_bank.models import BankAccount

from .utils import generate_random_code


class Card(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "AC", "Active"
        DISABLED = "DS", "Disable"
        CANCELLED = "CN", "Cancelled"

    card_name = models.CharField(max_length=50, primary_key=False, default='Founds')
    card_validation_code = generate_random_code(3)
    card_account_code = models.CharField(max_length=20, null=False, blank=True, default="C5-0001")
    status = models.CharField(max_length=20, default=Status.ACTIVE, choices=Status.choices)
    account = models.ForeignKey(BankAccount, on_delete=models.PROTECT)

    class Meta:
        ordering = ["-card_account_code"]
        indexes = [
            models.Index(fields=["-card_account_code"]),
        ]

    def save(self, *args, **kwargs) -> None:
        card_prefix = "C5"
        if not self.card_account_code:
            try:
                last_used_card_code = Card.objects.latest("card_account_code").card_account_code
                new_card_account_code = (
                    f"{card_prefix}-{int(last_used_card_code[3:].lstrip('0')) + 1:04d}"
                )
            except Card.DoesNotExist:
                new_card_account_code = "C5-0001"
            self.card_account_code = new_card_account_code
        return super(__class__, self).save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('card:card_detail', args=[self.id])


"""
<a href="{% url 'card_detail' card_account_code='card_account_code' %}"><p class="navbar-text navbar-right">Cards</p></a>
"""
