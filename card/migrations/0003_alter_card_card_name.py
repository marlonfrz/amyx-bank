# Generated by Django 4.2.6 on 2023-11-08 15:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('card', '0002_alter_card_account'),
    ]

    operations = [
        migrations.AlterField(
            model_name='card',
            name='card_name',
            field=models.CharField(default='Founds', max_length=50),
        ),
    ]
