# Generated by Django 4.2.7 on 2024-07-11 15:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0010_remove_company_payment_signature_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_payment',
            name='order_id',
            field=models.TextField(null=True),
        ),
        migrations.AddField(
            model_name='company_payment',
            name='signature',
            field=models.TextField(null=True),
        ),
    ]
