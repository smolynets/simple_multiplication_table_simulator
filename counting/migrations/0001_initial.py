# Generated by Django 3.1.4 on 2021-01-01 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='FinishPerDay',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finish_time', models.CharField(max_length=50)),
                ('score', models.CharField(max_length=10)),
                ('spended_time', models.CharField(max_length=1000)),
            ],
        ),
        migrations.CreateModel(
            name='SiteConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('greeting_text', models.TextField()),
            ],
            options={
                'verbose_name': 'Site Configuration',
            },
        ),
    ]
