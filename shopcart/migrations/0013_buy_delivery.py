# Generated by Django 3.2.7 on 2022-03-27 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shopcart', '0012_remove_cartitems_quanprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='buy',
            name='delivery',
            field=models.CharField(default='no', max_length=20),
        ),
    ]
