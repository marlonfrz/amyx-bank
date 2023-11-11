from django.db import models
from card.models import Card
from account.models import BankAccount

class Transaction(models.Model):
    class TransactionType(models.TextChoices):
        OUTGOING = "OG", "OUTGOING"
        INCOMING = "IC", "INCOMING"

    account = models.ForeignKey(BankAccount, on_delete=models.PROTECT, null=True, blank=True)
    agent = models.CharField(max_length=60)
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

class Payment(models.Model):
    card = models.ForeignKey(Card, on_delete=models.PROTECT)
    business = models.CharField(max_length=60)
    concept = models.CharField(max_length=100, default='')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    kind = models.CharField(max_length=20, default='PAYMENTS')

    objects = models.Manager()

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
        ]


#       ID=4      #
# F transaccion   #
#                 #
# "Destinatario"  #
#                 #
#                 #
#    Concepto     #
#                 #
#                 #
#    cantidad     #
#                 #
#      Tipo       #
