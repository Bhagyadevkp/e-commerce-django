# Generated by Django 3.2.7 on 2022-03-25 20:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('shopcart', '0011_cartitems_quanprice'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='cartitems',
            name='quanprice',
        ),
    ]
