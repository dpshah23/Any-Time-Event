# Generated by Django 4.2.7 on 2024-07-06 01:19

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0002_regvol_skills'),
    ]

    operations = [
        migrations.AddField(
            model_name='event',
            name='creation_date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]