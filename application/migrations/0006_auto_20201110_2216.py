# Generated by Django 3.1.2 on 2020-11-11 04:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0005_remove_device_password'),
    ]

    operations = [
        migrations.AddField(
            model_name='seedbox',
            name='user',
            field=models.CharField(default='', max_length=20),
        ),
        migrations.AlterField(
            model_name='device',
            name='type',
            field=models.CharField(default='ssh', max_length=20),
        ),
    ]
