# Generated by Django 4.2.7 on 2024-07-08 17:36

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth1', '0015_alter_otps_expires_at_alter_resetpass_expires_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otps',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 8, 17, 41, 34, 933880, tzinfo=datetime.timezone.utc)),
        ),
        migrations.AlterField(
            model_name='resetpass',
            name='expires_at',
            field=models.DateTimeField(default=datetime.datetime(2024, 7, 8, 18, 36, 34, 937022, tzinfo=datetime.timezone.utc)),
        ),
    ]
