# Generated by Django 5.0.6 on 2024-07-01 10:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth1', '0007_remove_otps_usage_company_image_name_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='users',
            name='role',
            field=models.CharField(default=None, max_length=20),
        ),
        migrations.AlterField(
            model_name='otps',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 10, 21, 10, 368082, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='resetpass',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 1, 11, 16, 10, 368980, tzinfo=datetime.timezone.utc)),
        ),
    ]