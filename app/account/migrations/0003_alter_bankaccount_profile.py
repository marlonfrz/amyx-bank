# Generated by Django 4.2.8 on 2023-12-28 22:25

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('amyx_bank', '0001_initial'),
        ('account', '0002_rename_account_balance_bankaccount_balance'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bankaccount',
            name='profile',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='amyx_bank.profile'),
        ),
    ]
