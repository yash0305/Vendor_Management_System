# Generated by Django 5.0 on 2023-12-19 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_alter_purchaseorder_vendor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='purchaseorder',
            name='po_number',
            field=models.CharField(max_length=50, unique=True),
        ),
    ]
