# Generated by Django 5.0.6 on 2024-07-12 10:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0014_remove_company_payment_order_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_payment',
            name='company_id',
            field=models.CharField(null=True),
        ),
    ]
