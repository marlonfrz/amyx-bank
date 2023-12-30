from django.db import models
from django.urls import reverse

from amyx_bank.models import Profile

class BankAccount(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "AC", "Active"
        DISABLED = "DS", "Disable"
        CANCELLED = "CN", "Cancelled"

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, null=True, related_name="accounts")
    account_name = models.CharField(max_length=50, primary_key=False)
    balance = models.DecimalField(max_digits=7, decimal_places=2, default=0)
    account_code = models.CharField(max_length=20, null=False, blank=True)
    status = models.CharField(max_length=20, default=Status.ACTIVE, choices=Status.choices)
    objects = models.Manager()
    

    class Meta:
        ordering = ["-account_code"]
        indexes = [
            models.Index(fields=["-account_code"]),
        ]

    def save(self, *args, **kwargs) -> None:
        bank_prefix = "A5"
        if not self.account_code:
            try:
                last_used_account_code = BankAccount.objects.latest("account_code").account_code
                new_bank_account_code = (
                    f"{bank_prefix}-{int(last_used_account_code[3:].lstrip('0')) + 1:04d}"
                )
            except BankAccount.DoesNotExist:
                new_bank_account_code = "A5-0001"
            self.account_code = new_bank_account_code
        return super(__class__, self).save(*args, **kwargs)
    
    def __str__(self) -> str:
        return self.account_name

    def __repr__(self) -> str:
        return self.account_name

    def get_absolute_url(self):
        return reverse('account_detail', args=[self.id])

#href="{% url 'reverse' account_detail account.id %}"


