# Generated by Django 3.0.3 on 2020-04-26 09:51

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ekart_app', '0004_auto_20200426_1506'),
    ]

    operations = [
        migrations.AddField(
            model_name='images',
            name='main_img',
            field=models.CharField(choices=[('y', 'YES'), ('n', 'NO')], default='n', max_length=10),
        ),
        migrations.AlterField(
            model_name='orders',
            name='exp_ship_time',
            field=models.DateField(default=datetime.datetime(2020, 5, 3, 15, 21, 19, 880447)),
        ),
        migrations.AlterField(
            model_name='shipping',
            name='shipping_status',
            field=models.CharField(choices=[('y', 'YES'), ('y', 'NO')], max_length=10),
        ),
    ]
