# Generated by Django 4.2.6 on 2023-10-31 16:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amyx_bank', '0007_card_card_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='card_account_code',
            field=models.CharField(blank=True, default='C5-0001', max_length=20),
        ),
    ]