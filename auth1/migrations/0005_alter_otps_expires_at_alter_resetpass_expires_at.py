# Generated by Django 5.0.6 on 2024-07-04 08:42

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth1', '0004_alter_otps_expires_at_alter_resetpass_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otps',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 4, 8, 47, 59, 66157, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='resetpass',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 4, 9, 42, 59, 67157, tzinfo=datetime.timezone.utc)),
        ),
    ]
