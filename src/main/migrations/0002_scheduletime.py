# Generated by Django 3.2 on 2022-08-15 08:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ScheduleTime',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_day_time', models.IntegerField(verbose_name='Початок робочого дня')),
                ('end_day_time', models.IntegerField(verbose_name='Кінець робочого дня')),
            ],
        ),
    ]
