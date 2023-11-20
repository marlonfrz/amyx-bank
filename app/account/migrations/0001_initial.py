# Generated by Django 4.2.6 on 2023-11-09 23:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("amyx_bank", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="BankAccount",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("account_name", models.CharField(max_length=50)),
                (
                    "account_balance",
                    models.DecimalField(decimal_places=2, default=0, max_digits=7),
                ),
                ("account_code", models.CharField(blank=True, max_length=20)),
                (
                    "status",
                    models.CharField(
                        choices=[
                            ("AC", "Active"),
                            ("DS", "Disable"),
                            ("CN", "Cancelled"),
                        ],
                        default="AC",
                        max_length=20,
                    ),
                ),
                (
                    "profile",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="amyx_bank.profile",
                    ),
                ),
            ],
            options={
                "ordering": ["-account_code"],
                "indexes": [
                    models.Index(
                        fields=["-account_code"], name="account_ban_account_d9fa55_idx"
                    )
                ],
            },
        ),
    ]