from django.db import models
from card.models import Card
from django.urls import reverse


class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        OUTGOING = "OG", "OUTGOING"
        INCOMING = "IC", "INCOMING"

    agent = models.CharField(max_length=60)
    account = models.CharField(max_length=7, default="")
    concept = models.CharField(max_length=100, default='')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    kind = models.CharField(max_length=20, 
                default=TransactionType.OUTGOING, 
                choices=TransactionType.choices)
    objects = models.Manager()


    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
        ]
    
    def get_absolute_url(self):
        return reverse('transaction_detail', args=[self.id])


class Payment(models.Model):
    card = models.ForeignKey(Card, on_delete=models.PROTECT, related_name="payments")
    business = models.CharField(max_length=60)
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    kind = models.CharField(max_length=20, default='PAYMENTS')

    objects = models.Manager()

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
        ]

    def get_absolute_url(self):
        return reverse('payment_detail', args=[self.id])