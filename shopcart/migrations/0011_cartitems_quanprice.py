# Generated by Django 3.2.7 on 2022-03-25 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopcart', '0010_buy_username'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='quanprice',
            field=models.IntegerField(default=0),
        ),
    ]
