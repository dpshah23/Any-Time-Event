# Generated by Django 4.2.7 on 2024-07-12 16:16

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('redirection', '0004_alter_review_date'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='review',
            name='date',
        ),
    ]
