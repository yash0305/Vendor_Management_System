# Generated by Django 5.0 on 2024-01-08 14:01

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0005_alter_historicalperformance_average_response_time_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='VendorProfile',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('vendor', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='api.vendor')),
            ],
        ),
    ]
