# Generated by Django 4.2.6 on 2023-10-29 19:20

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cosx_home', '0003_alter_orders_order_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='orders',
            name='order_date',
            field=models.DateTimeField(default=datetime.datetime(2023, 10, 29, 19, 20, 44, 228722, tzinfo=datetime.timezone.utc)),
        ),
    ]
