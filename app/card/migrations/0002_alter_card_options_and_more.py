# Generated by Django 4.2.6 on 2023-11-10 23:07

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("card", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="card",
            options={"ordering": ["-card_code"]},
        ),
        migrations.RemoveIndex(
            model_name="card",
            name="card_card_card_ac_40fc4a_idx",
        ),
        migrations.RemoveField(
            model_name="card",
            name="card_account_code",
        ),
        migrations.AddField(
            model_name="card",
            name="card_code",
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddIndex(
            model_name="card",
            index=models.Index(
                fields=["-card_code"], name="card_card_card_co_a9216b_idx"
            ),
        ),
    ]
