from django.conf import settings
from django.db import models
from django.urls import reverse


class Profile(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'AC', 'Active'
        DISABLED = 'DS', 'Disable'
        CANCELLED = 'CN', 'Cancelled'

    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True, null=False)
    status = models.CharField(max_length=20, default=Status.ACTIVE, choices=Status.choices)
    objects = models.Manager()

    class Meta:
        ordering = ['-user']
        indexes = [
            models.Index(fields=['-user']),
        ]

    def __str__(self):
        return f'Profile of {self.user}'
