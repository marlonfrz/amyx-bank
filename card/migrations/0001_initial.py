# Generated by Django 4.2.6 on 2023-11-08 00:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    initial = True

    dependencies = [
        ("amyx_bank", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Card",
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
                ("card_name", models.CharField(default=None, max_length=50)),
                (
                    "card_account_code",
                    models.CharField(blank=True, default="C5-0001", max_length=20),
                ),
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
                    "account",
                    models.ForeignKey(
                        default=None,
                        on_delete=django.db.models.deletion.PROTECT,
                        to="amyx_bank.bankaccount",
                    ),
                ),
            ],
            options={
                "ordering": ["-card_account_code"],
                "indexes": [
                    models.Index(
                        fields=["-card_account_code"],
                        name="card_card_card_ac_40fc4a_idx",
                    )
                ],
            },
        ),
    ]
