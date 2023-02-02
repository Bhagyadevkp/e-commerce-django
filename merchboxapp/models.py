
from django.contrib.auth.models import User
from django.db.models.signals import post_save,pre_save

from django.db import models
from django.template.defaultfilters import slugify

# Create your models here.
from django.utils import timezone

from merchbox import settings



class catelog(models.Model):
    name=models.CharField(max_length=100,unique=True)
    slug=models.SlugField(max_length=100,unique=True)

    def __str__(self):
        return '{}'.format(self.name)

class subcatelog(models.Model):
    subcategoryname=models.CharField(max_length=100,unique=True)
    maincategoryname=models.ForeignKey(catelog, on_delete=models.CASCADE)

    def __str__(self):
        return '{}'.format(self.subcategoryname)


class additems(models.Model):
    prod_id=models.IntegerField(unique=True)
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True,blank=True,null=True)
    image1 = models.ImageField(upload_to='photo')
    image2 = models.ImageField(upload_to='photo', blank=True)
    image3 = models.ImageField(upload_to='photo', blank=True)
    image4 = models.ImageField(upload_to='photo', blank=True)
    desc = models.TextField()
    price = models.IntegerField()
    offerprice=models.IntegerField(blank=True,null=True)
    stock=models.IntegerField(blank=True,null=True)
    flag=models.IntegerField(blank=True,null=True)
    subcategory=models.CharField(max_length=100,default='null')
    dealer = models.CharField(max_length=150)
    phonenumber = models.BigIntegerField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    category = models.ForeignKey(catelog, on_delete=models.CASCADE)
    date = models.DateTimeField(default=timezone.now)
    expdate = models.DateTimeField(default=timezone.now)


    def __str__(self):
        return '{}'.format(self.name)

    def save(self, *args, **kwargs):
        if self.slug is  None:
            self.slug = slugify(self.prod_id)
        return super(additems, self).save(*args, **kwargs)

class merchshop(models.Model):
    shopname=models.CharField(max_length=200)
    user=models.ForeignKey(User, on_delete=models.CASCADE)
    phonenumber = models.BigIntegerField()
    shopimage1 = models.ImageField(upload_to='shop',blank=True)
    shopimage2 = models.ImageField(upload_to='shop', blank=True)
    shopimage3 = models.ImageField(upload_to='shop', blank=True)
    shopimage4 = models.ImageField(upload_to='shop', blank=True)
    location=models.CharField(max_length=100,default=True)
    city=models.CharField(max_length=100,default=True)
    district=models.CharField(max_length=100,default=True)
    dateadded=models.DateTimeField(default=timezone.now)
    productavailability=models.IntegerField(default=0)
    def __str__(self):
        return '{}'.format(self.shopname)
#
# class vehicle(models.Model):
#     name = models.CharField(max_length=100, unique=True)
#     slug = models.SlugField(max_length=100, unique=True)
#     user=models.ForeignKey(User,on_delete=models.CASCADE)
#
#     brand = models.CharField(max_length=150)
#     category=models.CharField(max_length=100)
#     year = models.IntegerField()
#     fuel = models.CharField(max_length=150)
#     image1 = models.ImageField(upload_to='car')
#     image2 = models.ImageField(upload_to='car',blank=True)
#     image3= models.ImageField(upload_to='car',blank=True)
#     image4 = models.ImageField(upload_to='car',blank=True)
#     transmission = models.CharField(max_length=100)
#     kmdriven = models.IntegerField()
#     owners = models.IntegerField()
#     desc = models.TextField()
#     price = models.IntegerField()
#     location = models.CharField(max_length=150)
#     city = models.CharField(max_length=150)
#     dealer=models.CharField(max_length=150)
#     phonenumber=models.BigIntegerField()
#
#     def __str__(self):
#         return '{}'.format(self.user)
#
# class propertie(models.Model):
#     name=models.CharField(max_length=100,unique=True)
#     slug=models.SlugField(max_length=100,unique=True)
#     location=models.CharField(max_length=100)
#     city=models.CharField(max_length=100)
#     title=models.CharField(max_length=100)
#     desc = models.TextField()
#     price = models.IntegerField()
#     image1 = models.ImageField(upload_to='property')
#     image2 = models.ImageField(upload_to='property', blank=True)
#     image3 = models.ImageField(upload_to='property', blank=True)
#     image4 = models.ImageField(upload_to='property', blank=True)
#     dealer = models.CharField(max_length=150)
#     phonenumber = models.BigIntegerField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return '{}'.format(self.user)
#
# class mobile(models.Model):
#     name=models.CharField(max_length=100,unique=True)
#     slug=models.SlugField(max_length=100,unique=True)
#     location = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     title = models.CharField(max_length=100)
#     type=models.CharField(max_length=100)
#     desc = models.TextField()
#     price = models.IntegerField()
#     image1 = models.ImageField(upload_to='property')
#     image2 = models.ImageField(upload_to='property', blank=True)
#     image3 = models.ImageField(upload_to='property', blank=True)
#     image4 = models.ImageField(upload_to='property', blank=True)
#     dealer = models.CharField(max_length=150)
#     phonenumber = models.BigIntegerField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return '{}'.format(self.user)
#
#
#
# class electronic_appliance(models.Model):
#     name=models.CharField(max_length=100,unique=True)
#     slug=models.SlugField(max_length=100,unique=True)
#     location = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     title = models.CharField(max_length=100)
#     type = models.CharField(max_length=100)
#     desc = models.TextField()
#     price = models.IntegerField()
#     image1 = models.ImageField(upload_to='property')
#     image2 = models.ImageField(upload_to='property', blank=True)
#     image3 = models.ImageField(upload_to='property', blank=True)
#     image4 = models.ImageField(upload_to='property', blank=True)
#     dealer = models.CharField(max_length=150)
#     phonenumber = models.BigIntegerField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return '{}'.format(self.user)
#
# class household_appliance(models.Model):
#     name=models.CharField(max_length=100,unique=True)
#     slug=models.SlugField(max_length=100,unique=True)
#     location = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     title = models.CharField(max_length=100)
#     type = models.CharField(max_length=100)
#     desc = models.TextField()
#     price = models.IntegerField()
#     image1 = models.ImageField(upload_to='property')
#     image2 = models.ImageField(upload_to='property', blank=True)
#     image3 = models.ImageField(upload_to='property', blank=True)
#     image4 = models.ImageField(upload_to='property', blank=True)
#     dealer = models.CharField(max_length=150)
#     phonenumber = models.BigIntegerField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return '{}'.format(self.user)
#
# class costume(models.Model):
#     name=models.CharField(max_length=100,unique=True)
#     slug=models.SlugField(max_length=100,unique=True)
#     location = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     title = models.CharField(max_length=100)
#     section = models.CharField(max_length=100)
#     type = models.CharField(max_length=100)
#     desc = models.TextField()
#     price = models.IntegerField()
#     image1 = models.ImageField(upload_to='property')
#     image2 = models.ImageField(upload_to='property', blank=True)
#     image3 = models.ImageField(upload_to='property', blank=True)
#     image4 = models.ImageField(upload_to='property', blank=True)
#     dealer = models.CharField(max_length=150)
#     phonenumber = models.BigIntegerField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return '{}'.format(self.user)
#
# class pet(models.Model):
#     name=models.CharField(max_length=100,unique=True)
#     slug=models.SlugField(max_length=100,unique=True)
#     location = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     title = models.CharField(max_length=100)
#     type = models.CharField(max_length=100)
#     desc = models.TextField()
#     price = models.IntegerField()
#     image1 = models.ImageField(upload_to='property')
#     image2 = models.ImageField(upload_to='property', blank=True)
#     image3 = models.ImageField(upload_to='property', blank=True)
#     image4 = models.ImageField(upload_to='property', blank=True)
#     dealer = models.CharField(max_length=150)
#     phonenumber = models.BigIntegerField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return '{}'.format(self.user)
#
# class wholesale(models.Model):
#     name=models.CharField(max_length=100,unique=True)
#     slug=models.SlugField(max_length=100,unique=True)
#     location = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     title = models.CharField(max_length=100)
#     type = models.CharField(max_length=100)
#     desc = models.TextField()
#     price = models.IntegerField()
#     image1 = models.ImageField(upload_to='property')
#     image2 = models.ImageField(upload_to='property', blank=True)
#     image3 = models.ImageField(upload_to='property', blank=True)
#     image4 = models.ImageField(upload_to='property', blank=True)
#     dealer = models.CharField(max_length=150)
#     phonenumber = models.BigIntegerField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return '{}'.format(self.user)
#
# class grocerie(models.Model):
#     name=models.CharField(max_length=100,unique=True)
#     slug=models.SlugField(max_length=100,unique=True)
#     location = models.CharField(max_length=100)
#     city = models.CharField(max_length=100)
#     title = models.CharField(max_length=100)
#     type = models.CharField(max_length=100)
#     desc = models.TextField()
#     price = models.IntegerField()
#     image1 = models.ImageField(upload_to='property')
#     image2 = models.ImageField(upload_to='property', blank=True)
#     image3 = models.ImageField(upload_to='property', blank=True)
#     image4 = models.ImageField(upload_to='property', blank=True)
#     dealer = models.CharField(max_length=150)
#     phonenumber = models.BigIntegerField()
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#
#     def __str__(self):
#         return '{}'.format(self.user)
#
#
# # sub categories
#
#
# # class photos(models.Model):
# #     user = models.ForeignKey(User, on_delete=models.CASCADE)
# #     newimage=models.ImageField(upload_to='pics')
# #
# #
# #     def __str__(self):
# #         return '{}'.format(self.user)
#
#
#
#
