# Generated by Django 3.1.2 on 2020-11-14 04:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0012_auto_20201112_1652'),
    ]

    operations = [
        migrations.CreateModel(
            name='LogEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entry', models.CharField(default='', max_length=500)),
                ('created', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]