# Generated by Django 4.2.7 on 2024-07-06 04:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0003_event_creation_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='is_paid_vol',
            field=models.BooleanField(default=False),
        ),
    ]
