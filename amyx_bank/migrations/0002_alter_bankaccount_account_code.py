# Generated by Django 4.2.6 on 2023-11-08 17:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('amyx_bank', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='account_code',
            field=models.CharField(blank=True, max_length=20),
        ),
    ]
