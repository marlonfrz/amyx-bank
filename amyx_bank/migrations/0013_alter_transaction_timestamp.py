# Generated by Django 4.2.6 on 2023-11-04 13:30

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("amyx_bank", "0012_alter_bankaccount_options_alter_card_options_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="transaction",
            name="timestamp",
            field=models.DateTimeField(auto_now_add=True),
        ),
    ]
