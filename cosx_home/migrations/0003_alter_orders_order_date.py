# Generated by Django 4.1.2 on 2023-06-25 09:43

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("cosx_home", "0002_alter_orders_order_date"),
    ]

    operations = [
        migrations.AlterField(
            model_name="orders",
            name="order_date",
            field=models.DateTimeField(
                default=datetime.datetime(
                    2023, 6, 25, 9, 43, 42, 440166, tzinfo=datetime.timezone.utc
                )
            ),
        ),
    ]
