# Generated by Django 2.0 on 2019-01-09 14:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('dorm', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Building',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(default='', max_length=100, verbose_name='number')),
                ('high', models.IntegerField(verbose_name='high')),
                ('room', models.IntegerField(verbose_name='room')),
                ('begintime', models.DateTimeField(verbose_name='begintime')),
            ],
        ),
    ]
