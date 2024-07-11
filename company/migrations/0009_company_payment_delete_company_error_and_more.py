# Generated by Django 5.0.6 on 2024-07-11 08:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('company', '0008_alter_regvol_attendence'),
    ]

    operations = [
        migrations.CreateModel(
            name='company_payment',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateField()),
                ('payment_id', models.TextField()),
                ('signature', models.TextField()),
            ],
        ),
        migrations.DeleteModel(
            name='company_error',
        ),
        migrations.DeleteModel(
            name='company_success',
        ),
    ]
