# Generated by Django 4.2.7 on 2024-07-12 16:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('redirection', '0002_review'),
    ]

    operations = [
        migrations.AddField(
            model_name='review',
            name='date',
            field=models.DateField(default=None),
        ),
    ]
