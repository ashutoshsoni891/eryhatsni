# Generated by Django 4.1 on 2022-08-10 07:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('spamCheckerApp', '0002_profile_username'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='phone',
            field=models.CharField(max_length=13, unique=True),
        ),
    ]