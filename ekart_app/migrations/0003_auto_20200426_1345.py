# Generated by Django 3.0.3 on 2020-04-26 08:15

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ekart_app', '0002_auto_20200426_1321'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='exp_ship_time',
            field=models.DateField(default=datetime.datetime(2020, 5, 3, 13, 45, 21, 397666)),
        ),
    ]
