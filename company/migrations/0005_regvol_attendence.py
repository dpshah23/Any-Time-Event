# Generated by Django 5.0.6 on 2024-07-06 08:23

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0004_event_is_paid_vol'),
    ]

    operations = [
        migrations.AddField(
            model_name='regvol',
            name='attendence',
            field=models.BooleanField(default=False),
        ),
    ]
