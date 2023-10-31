from django.conf import settings
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date_of_birth = models.DateField(blank=True, null=True)
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

    # class Meta:
    #    ordering = ['-movement']
    #    indexes = [
    #        models.Index(fields=['-movement']),
    #    ]

    # NO TOCAR EL METODO SAVE; FUNCIONA BIEN
    """ def save(self, *args, **kwargs) -> None:
        bank_prefix = "A5"
        last_used_account_code = BankAccount.objects.latest("account_code").account_code
        new_bank_account_code = (
            f"{bank_prefix}-{int(last_used_account_code[3:].lstrip('0')) + 1:04d}"
        )
        self.account_code = new_bank_account_code
        return super(__class__, self).save(*args, **kwargs) """

    def save(self, *args, **kwargs):
        if not self.account_code:
            bank_prefix = "A5"
            last_used_account = BankAccount.objects.order_by('-account_code').first()
            if last_used_account:
                last_code = last_used_account.account_code
                new_account_code = f"{bank_prefix}-{int(last_code[3:].lstrip('0')) + 1:04d}"
            else:
                new_account_code = "A5-0001"
            self.account_code = new_account_code
        super(BankAccount, self).save(*args, **kwargs)

    # adaptar y crear view de account_detail


#    def get_absolute_url(self):
#        return reverse('amyx_bank:account_detail', args=[self.id])


class Card(models.Model):
    pass
