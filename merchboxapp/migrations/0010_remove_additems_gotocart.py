# Generated by Django 3.2.7 on 2022-02-19 18:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('merchboxapp', '0009_additems_gotocart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='additems',
            name='gotocart',
        ),
    ]
