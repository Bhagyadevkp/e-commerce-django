# Generated by Django 3.2.7 on 2022-03-27 08:49

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('shopcart', '0013_buy_delivery'),
    ]

    operations = [
        migrations.AddField(
            model_name='buy',
            name='dateadded',
            field=models.DateTimeField(default=datetime.datetime(2022, 3, 27, 8, 49, 2, 707423, tzinfo=utc)),
        ),
    ]
