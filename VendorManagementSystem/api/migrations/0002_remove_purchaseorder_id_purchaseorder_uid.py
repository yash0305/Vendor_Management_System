# Generated by Django 5.0 on 2023-12-14 15:52

import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='purchaseorder',
            name='id',
        ),
        migrations.AddField(
            model_name='purchaseorder',
            name='uid',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
    ]
