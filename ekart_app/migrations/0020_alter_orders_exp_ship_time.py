# Generated by Django 5.2 on 2025-04-19 18:08

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ekart_app', '0019_alter_orders_exp_ship_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='exp_ship_time',
            field=models.DateField(default=datetime.datetime(2025, 4, 26, 23, 38, 13, 846313)),
        ),
    ]
