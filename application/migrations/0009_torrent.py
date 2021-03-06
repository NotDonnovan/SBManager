# Generated by Django 3.1.2 on 2020-11-12 05:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('application', '0008_auto_20201111_2241'),
    ]

    operations = [
        migrations.CreateModel(
            name='Torrent',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='N/A', max_length=200)),
                ('state', models.CharField(default='', max_length=50)),
                ('progress', models.IntegerField()),
                ('size', models.CharField(default='', max_length=10)),
                ('ratio', models.FloatField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='torrent_category', to='application.category')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='torrent_client', to='application.seedbox')),
            ],
        ),
    ]
