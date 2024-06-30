# Generated by Django 4.2.7 on 2024-06-30 08:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth1', '0005_visit'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='visit',
            name='visit_timestamp',
        ),
        migrations.RemoveField(
            model_name='visit',
            name='visitor_country',
        ),
        migrations.RemoveField(
            model_name='visit',
            name='visitor_ip',
        ),
        migrations.AddField(
            model_name='visit',
            name='visit_count',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='visit',
            name='page_visited',
            field=models.CharField(max_length=255, unique=True),
        ),
    ]