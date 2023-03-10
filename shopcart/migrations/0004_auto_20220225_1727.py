# Generated by Django 3.2.7 on 2022-02-25 11:57

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('shopcart', '0003_cartitems_dateadded'),
    ]

    operations = [
        migrations.AddField(
            model_name='cartitems',
            name='price',
            field=models.IntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='cartitems',
            name='dateadded',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
