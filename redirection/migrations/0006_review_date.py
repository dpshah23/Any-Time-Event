# Generated by Django 4.2.7 on 2024-07-12 16:18

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redirection', '0005_remove_review_date'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='date',
            field=models.DateField(default=datetime.date.today),
        ),
    ]
