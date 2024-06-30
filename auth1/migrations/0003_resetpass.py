# Generated by Django 5.0.6 on 2024-06-28 10:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auth1', '0002_company_volunteer'),
    ]

    operations = [
        migrations.CreateModel(
            name='resetpass',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=100)),
                ('keys', models.TextField()),
                ('usage', models.BooleanField(default=False)),
            ],
        ),
    ]