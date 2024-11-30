# Generated by Django 5.1.3 on 2024-11-30 19:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0001_initial'),
        ('posts', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='post',
            name='genres',
            field=models.ManyToManyField(related_name='posts', to='accounts.genre'),
        ),
    ]
