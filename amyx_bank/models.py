from django.conf import settings
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date_of_birth = models.DateField(blank=True, null=True)
    #accounts = models.ManyToOneRel()

    def __str__(self):
        return f'Profile of {self.user.username}'


class BankAccount(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'AC', 'Active'
        DISABLED = 'DS', 'Disable'
        CANCELLED = 'CN', 'Cancelled'

    account_name = models.CharField(max_length=50, primary_key=False)
    account_balance = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    status = models.CharField(max_length=20)
    objects = models.Manager()


    #    class Meta:
    #        ordering = ['-movement']
    #        indexes = [
    #            models.Index(fields=['-movement']),
    #        ]

    def save(self, *args, **kwargs) -> None:
        try:
            last_used_id = BankAccount.objects.latest("id")
            new_bank_account_code = last_used_id + 1
            self.account_code = f"A5-{new_bank_account_code:04d}"
        except BankAccount.DoesNotExist:
            self.account_code = "A5-0001"
        self._meta.get_field('account_balance').editable = False
        return super().save(self, *args, **kwargs)

    # adaptar y crear view de account_detail


#    def get_absolute_url(self):
#        return reverse('amyx_bank:account_detail', args=[self.id])


class Card(models.Model):
    pass
