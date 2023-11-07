from django.contrib.auth.models import User
from django.db import models


class Profile(models.Model):
    class Status(models.TextChoices):
        ACTIVE = 'AC', 'Active'
        DISABLED = 'DS', 'Disable'
        CANCELLED = 'CN', 'Cancelled'

    user = models.OneToOneField(User, on_delete=models.PROTECT, related_name='profile')
    date_of_birth = models.DateField(blank=True, null=True)
    avatar = models.ImageField(upload_to='users/%Y/%m/%d/', blank=True)
    status = models.CharField(max_length=20, default=Status.ACTIVE, choices=Status.choices)
    objects = models.Manager()

    class Meta:
        ordering = ['-user']
        indexes = [
            models.Index(fields=['-user']),
        ]

    def __str__(self):
        return f'Profile of {self.user}'


class DeletedUser(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=False, null=True, default=None)
    deleted_date = models.DateTimeField(auto_now=True)
