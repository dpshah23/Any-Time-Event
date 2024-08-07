# Generated by Django 4.2.7 on 2024-07-14 17:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0016_company_payment_amount_company_payment_event_date_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='company_payment',
            name='order_id',
            field=models.TextField(default=None),
        ),
        migrations.AddField(
            model_name='company_payment',
            name='signature',
            field=models.TextField(default=None),
        ),
        migrations.AlterField(
            model_name='company_payment',
            name='payment_id',
            field=models.TextField(default=None),
        ),
    ]
