# Generated by Django 5.0.6 on 2024-07-04 09:36

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_email', models.CharField(max_length=150, null=True)),
                ('event_company', models.CharField(max_length=200, null=True)),
                ('event_name', models.CharField(max_length=200)),
                ('event_id', models.CharField(default=False, max_length=100, unique=True)),
                ('event_date', models.DateField()),
                ('event_time', models.TimeField()),
                ('event_end_time', models.TimeField(null=True)),
                ('event_location', models.CharField(max_length=100)),
                ('event_loc_link', models.CharField(max_length=400, null=True)),
                ('event_city', models.CharField(max_length=100, null=True)),
                ('event_description', models.TextField(max_length=1000)),
                ('event_skills', models.CharField(max_length=200)),
                ('event_rep', models.CharField(max_length=200, null=True)),
                ('event_rep_no', models.CharField(max_length=15, null=True)),
                ('event_vol', models.IntegerField()),
                ('event_completed', models.BooleanField(default=False)),
                ('event_mrp', models.IntegerField(null=True)),
                ('actual_amount', models.IntegerField(null=True)),
                ('paid_status', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RegVol',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('company_email', models.CharField(max_length=200, null=True)),
                ('event_id_1', models.CharField(max_length=100, null=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=100)),
                ('phone', models.CharField(max_length=100)),
                ('paid_status', models.BooleanField()),
            ],
        ),
    ]
