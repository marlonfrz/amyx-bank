# Generated by Django 4.2.6 on 2023-11-12 19:21

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("payment", "0004_alter_transaction_account"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="payment",
            name="concept",
        ),
    ]
