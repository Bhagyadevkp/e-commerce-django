# Generated by Django 3.2.7 on 2022-01-12 14:17

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('merchboxapp', '0003_delete_check'),
    ]

    operations = [
        migrations.CreateModel(
            name='additems',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('prod_id', models.IntegerField()),
                ('name', models.CharField(max_length=100, unique=True)),
                ('slug', models.SlugField(blank=True, max_length=100, null=True, unique=True)),
                ('image1', models.ImageField(upload_to='photo')),
                ('image2', models.ImageField(blank=True, upload_to='photo')),
                ('image3', models.ImageField(blank=True, upload_to='photo')),
                ('image4', models.ImageField(blank=True, upload_to='photo')),
                ('desc', models.TextField()),
                ('price', models.IntegerField()),
                ('location', models.CharField(max_length=150)),
                ('city', models.CharField(max_length=150)),
                ('dealer', models.CharField(max_length=150)),
                ('phonenumber', models.BigIntegerField()),
                ('title', models.CharField(max_length=100)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('expdate', models.DateTimeField(default=django.utils.timezone.now)),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='merchboxapp.catelog')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='merchshop',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('shopname', models.CharField(max_length=200)),
                ('phonenumber', models.BigIntegerField()),
                ('shopimage', models.ImageField(blank=True, upload_to='shop')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.DeleteModel(
            name='newproducts',
        ),
    ]
