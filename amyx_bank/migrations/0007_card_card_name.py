# Generated by Django 4.2.6 on 2023-10-31 16:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amyx_bank', '0006_alter_bankaccount_account_code'),
    ]

    operations = [
        migrations.AddField(
            model_name='card',
            name='card_name',
            field=models.CharField(default=None, max_length=50),
        ),
    ]