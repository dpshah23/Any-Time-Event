# Generated by Django 4.2.7 on 2024-07-15 15:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0022_company_payment_order_id_company_payment_signature_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='company_id',
            field=models.CharField(max_length=150, null=True),
        ),
    ]
