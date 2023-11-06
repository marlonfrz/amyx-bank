from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType
from django.db import models


class Transaction(models.Model):
    agent = models.CharField(max_length=60)
    concept = models.CharField(max_length=100, default='')
    amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    timestamp = models.DateTimeField(auto_now_add=True)
    kind = models.CharField(max_length=20, default='buy')

    objects = models.Manager()
    target_ct = models.ForeignKey(
        ContentType, blank=True, null=True, related_name='transactions', on_delete=models.PROTECT
    )
    target_id = models.PositiveIntegerField(null=True, blank=True)
    target = GenericForeignKey('target_ct', 'target_id')

    class Meta:
        ordering = ['-timestamp']
        indexes = [
            models.Index(fields=['-timestamp']),
            models.Index(fields=['target_ct', 'target_id']),
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
