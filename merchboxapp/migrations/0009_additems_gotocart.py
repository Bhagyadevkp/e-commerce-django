# Generated by Django 3.2.7 on 2022-02-19 18:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('merchboxapp', '0008_auto_20220116_1131'),
    ]

    operations = [
        migrations.AddField(
            model_name='additems',
            name='gotocart',
            field=models.IntegerField(default=0),
        ),
    ]