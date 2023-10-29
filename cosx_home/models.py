from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.dispatch import receiver    
from django.db.models.signals import post_save


# Create your models here.

class Products(models.Model):
    p_name = models.CharField(max_length=100)
    p_rating = models.DecimalField(max_digits=5, decimal_places=1)
    p_description = models.CharField(max_length=500)
    p_buycount = models.IntegerField()
    p_brand = models.CharField(max_length=100)
    p_category = models.CharField(max_length=100)
    p_image = models.ImageField(upload_to="static/images/")
    p_price = models.DecimalField(max_digits=7, decimal_places=2)

    
class Orders(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)
    order_date = models.DateTimeField(default=timezone.now())
    phoneNum = models.CharField(max_length=15, default="+911234567890")
    email = models.EmailField(max_length=50, default="johndoe@email.com")
    price = models.DecimalField(max_digits=7, decimal_places=2)
    addr1 = models.CharField(max_length=200)
    fname = models.CharField(max_length=100, default="John")
    lname = models.CharField(max_length=100, default="Doe")



class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

class Wallet(models.Model):
    user = models.ForeignKey(User, unique=True, on_delete=models.CASCADE)
    wallet = models.DecimalField(max_digits=7, decimal_places=2, default=10000.00)

class Rating(models.Model):
    order = models.ForeignKey(Orders, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)