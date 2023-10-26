from django.conf import settings
from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date_of_birth = models.DateField(blank=True, null=True)

    def __str__(self):
        return f'Profile of {self.user.username}'

class BankAccount(models.Model):
    account_name = models.CharField(max_length=20)

class Meta:
    ordering = []
