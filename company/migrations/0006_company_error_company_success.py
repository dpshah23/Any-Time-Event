# Generated by Django 5.0.6 on 2024-07-06 09:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0005_regvol_attendence'),
    ]

    operations = [
        migrations.CreateModel(
            name='company_error',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateField()),
                ('code', models.TextField()),
                ('description', models.TextField()),
                ('reason', models.TextField()),
            ],
        ),
        migrations.CreateModel(
            name='company_success',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateField()),
                ('payment_id', models.TextField()),
                ('order_id', models.TextField()),
                ('signature', models.TextField()),
            ],
        ),
    ]