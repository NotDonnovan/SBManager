# Generated by Django 3.1.2 on 2020-11-11 02:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0004_auto_20201110_0039'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='device',
            name='password',
        ),
    ]
