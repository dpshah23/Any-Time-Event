# Generated by Django 4.2.7 on 2024-07-07 05:37

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth1', '0011_alter_otps_expires_at_alter_resetpass_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otps',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 7, 5, 42, 48, 770095, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='resetpass',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 7, 6, 37, 48, 770095, tzinfo=datetime.timezone.utc)),
        ),
    ]