# Generated by Django 4.2.7 on 2024-07-12 10:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0012_remove_company_payment_signature_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='company_payment',
            name='status',
            field=models.BooleanField(default=False),
        ),
    ]
