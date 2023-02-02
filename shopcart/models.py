import datetime

import django
from django.db import models

# Create your models here.
from django.db import models

# Create your models here.
from django.utils import timezone

from merchboxapp.models import additems


class cart(models.Model):
    cart_id=models.CharField(max_length=250,unique=True)
    date_added=models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.cart_id

class cartitems(models.Model):
    cartproduct=models.CharField(max_length=200)
    cart=models.IntegerField()
    productid = models.IntegerField(default=0000)

    quantity=models.IntegerField()
    available=models.IntegerField(default=1)
    price=models.IntegerField(default=0)
    dateadded=models.DateTimeField(default=django.utils.timezone.now)

    def __str__(self):
        return str(self.cartproduct)

class buy(models.Model):
    purchaser=models.CharField(max_length=200)
    username=models.CharField(max_length=100,default='not given')
    email=models.CharField(max_length=200)
    phonenumber=models.CharField(max_length=200)
    housename=models.CharField(max_length=200)
    area=models.CharField(max_length=200)
    location=models.CharField(max_length=200)
    district=models.CharField(max_length=200)
    pin=models.IntegerField()
    delivery=models.CharField(max_length=20,default='no')

    productid=models.IntegerField()
    productname=models.CharField(max_length=200)
    shopname=models.CharField(max_length=200)
    sellinguser=models.CharField(max_length=200,default='not given')
    quantity=models.IntegerField()
    price=models.IntegerField()
    totalprice=models.IntegerField()
    dateadded=models.DateTimeField(default=timezone.now)

    def __str__(self):
        return str(self.username)




