from django.conf import settings
from django.core.mail import send_mail
from django.db import models
from django.urls import reverse

from account.models import Profile

from .utils import generate_random_code


# USER User
#
# PROFILE Profile
#
# CUENTAS DE BANCO BankAccount
#
# CARD Card
#
class BankAccount(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'AC', 'Active'
        DISABLED = 'DS', 'Disable'
        CANCELLED = 'CN', 'Cancelled'

    account = models.OneToOneField(
        settings.AUTH_USER_MODEL, related_name='bank_accounts', on_delete=models.PROTECT, null=True
    )
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True)
    account_name = models.CharField(max_length=50, primary_key=False)
    account_balance = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    account_code = models.CharField(max_length=20, null=False, blank=True, default="A5-0001")
    status = models.CharField(max_length=20, default=Status.ACTIVE, choices=Status.choices)
    objects = models.Manager()

    class Meta:
        ordering = ['-account_code']
        indexes = [
            models.Index(fields=['-account_code']),
        ]

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
    class Status(models.TextChoices):
        ACTIVE = 'AC', 'Active'
        DISABLED = 'DS', 'Disable'
        CANCELLED = 'CN', 'Cancelled'

    card_name = models.CharField(max_length=50, primary_key=False, default=None)
    card_validation_code = generate_random_code(3)
    card_account_code = models.CharField(max_length=20, null=False, blank=True, default="C5-0001")
    status = models.CharField(max_length=20, default=Status.ACTIVE, choices=Status.choices)

    account = models.ForeignKey(
        BankAccount, related_name='cards', on_delete=models.PROTECT, null=True
    )

    class Meta:
        ordering = ['-card_account_code']
        indexes = [
            models.Index(fields=['-card_account_code']),
        ]

    def save(self, *args, **kwargs) -> None:
        card_prefix = "C5"
        try:
            last_used_card_code = Card.objects.latest("card_account_code").card_account_code
            new_card_account_code = (
                f"{card_prefix}-{int(last_used_card_code[3:].lstrip('0')) + 1:04d}"
            )
        except Card.DoesNotExist:
            new_card_account_code = "C5-0001"
        # print(self.account.profile.user.email)
        #        send_mail('Your credit has been created',f'Your credit card has the code {self.card_validation_code}',settings.EMAIL_HOST_USER,[self.account.profile.user.email], fail_silently=True,)
        self.card_account_code = new_card_account_code
        return super(__class__, self).save(*args, **kwargs)
