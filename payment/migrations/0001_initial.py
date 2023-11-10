# Generated by Django 4.2.6 on 2023-11-08 14:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
    ]

    operations = [
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('agent', models.CharField(max_length=60)),
                ('concept', models.CharField(default='', max_length=100)),
                ('amount', models.DecimalField(decimal_places=2, default=0, max_digits=10)),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
                ('kind', models.CharField(default='buy', max_length=20)),
                ('target_id', models.PositiveIntegerField(blank=True, null=True)),
                ('target_ct', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='transactions', to='contenttypes.contenttype')),
            ],
            options={
                'ordering': ['-timestamp'],
                'indexes': [models.Index(fields=['-timestamp'], name='payment_tra_timesta_7eb871_idx'), models.Index(fields=['target_ct', 'target_id'], name='payment_tra_target__1243c8_idx')],
            },
        ),
    ]
