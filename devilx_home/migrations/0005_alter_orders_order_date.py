# Generated by Django 4.2.6 on 2023-10-29 20:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('devilx_home', '0004_alter_orders_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(
                2023, 10, 29, 20, 53, 10, 257161, tzinfo=datetime.timezone.utc)),
        ),
    ]
