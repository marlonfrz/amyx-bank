# Generated by Django 4.2.7 on 2023-11-04 20:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('amyx_bank', '0015_card_status_profile_status'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='target_ct',
        ),
        migrations.RemoveField(
            model_name='profile',
            name='user',
        ),
        migrations.DeleteModel(
            name='deleted_user',
        ),
        migrations.DeleteModel(
            name='Profile',
        ),
    ]
