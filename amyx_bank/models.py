from django.conf import settings
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date_of_birth = models.DateField(blank=True, null=True)
    # accounts = models.ManyToOneRel()

    def __str__(self):
        return f'Profile of {self.user.username}'


class BankAccount(models.Model):
    objects = models.Manager()
    account_name = models.CharField(max_length=50, primary_key=False)

    class Status(models.TextChoices):
        ACTIVE = 'AC', 'Active'
        DISABLE = 'DS', 'Disable'
        CANCELLED = 'CN', 'Cancelled'

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
        return super().save(self, *args, **kwargs)

    # adaptar y crear view de account_detail


#    def get_absolute_url(self):
#        return reverse('amyx_bank:account_detail', args=[self.id])


class Card(models.Model):
    pass
