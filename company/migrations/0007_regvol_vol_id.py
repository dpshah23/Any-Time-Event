# Generated by Django 5.0.6 on 2024-07-06 16:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0006_company_error_company_success'),
    ]

    operations = [
        migrations.AddField(
            model_name='regvol',
            name='vol_id',
            field=models.CharField(max_length=100, null=True),
        ),
    ]
