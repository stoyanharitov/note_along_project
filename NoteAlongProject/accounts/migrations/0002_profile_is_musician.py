# Generated by Django 5.1.3 on 2024-12-03 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='is_musician',
            field=models.BooleanField(default=False),
        ),
    ]