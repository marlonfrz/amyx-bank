from django.conf import settings

# from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models

from .utils import generate_random_code


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date_of_birth = models.DateField(blank=True, null=True)
    # reporter = models.ForeignKey(Reporter, on_delete=models.CASCADE)
    # ccounts = models.ManyToOneRel()

    def __str__(self):
        return f'Profile of {self.user}'


class BankAccount(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'AC', 'Active'
        DISABLED = 'DS', 'Disable'
        CANCELLED = 'CN', 'Cancelled'

    account_name = models.CharField(max_length=50, primary_key=False)
    account_balance = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    account_code = models.CharField(max_length=20, null=False, blank=True, default="A5-0001")
    status = models.CharField(max_length=20, default=Status.ACTIVE, choices=Status.choices)
    objects = models.Manager()
    target_ct = models.ForeignKey(
        ContentType, blank=True, null=True, related_name='target_obj', on_delete=models.PROTECT
    )
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_ct', 'target_id')

    # = models.ForeignKey(Reporter, on_delete=models.CASCADE)

    # class Meta:
    #    ordering = ['-movement']
    #    indexes = [
    #        models.Index(fields=['-movement']),
    #        models.Index(fields=['target_ct', 'target_id']),
    #    ]
    # NO TOCAR EL METODO SAVE; FUNCIONA BIEN

    def save(self, *args, **kwargs) -> None:
        bank_prefix = "A5"
        try:
            last_used_account_code = BankAccount.objects.latest("account_code").account_code
            new_bank_account_code = (
                f"{bank_prefix}-{int(last_used_account_code[3:].lstrip('0')) + 1:04d}"
            )
        except BankAccount.DoesNotExist:
            new_bank_account_code = "A5-0001"
        self.account_code = new_bank_account_code
        return super(__class__, self).save(*args, **kwargs)


#    def get_absolute_url(self):
#        return reverse('amyx_bank:account_detail', args=[self.id])


class Card(models.Model):
    card_name = models.CharField(max_length=50, primary_key=False, default=None)
    card_validation_code = generate_random_code(3)
    card_account_code = models.CharField(max_length=20, null=False, blank=True, default="C5-0001")

    def save(self, *args, **kwargs) -> None:
        card_prefix = "C5"
        try:
            last_used_card_code = Card.objects.latest("card_account_code").card_account_code
            new_card_account_code = (
                f"{card_prefix}-{int(last_used_card_code[3:].lstrip('0')) + 1:04d}"
            )
        except Card.DoesNotExist:
            new_card_account_code = "C5-0001"
        self.card_account_code = new_card_account_code
        return super(__class__, self).save(*args, **kwargs)


class Transaction(models.Model):
    agent = models.CharField(max_length=60)
    pass


class deleted_user(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=True, default=None
    )
    deleted_date = models.DateTimeField(auto_now=True)
