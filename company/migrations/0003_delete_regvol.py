# Generated by Django 5.0.6 on 2024-07-04 08:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_regvol_remove_event_security_deposite_and_more'),
    ]

    operations = [
        migrations.DeleteModel(
            name='RegVol',
        ),
    ]
