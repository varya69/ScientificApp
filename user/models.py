from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms

# class User(AbstractUser):
#     ROLE_CHOICES = (
#         ('seller', 'Seller'),
#         ('user', 'User'),
#     )
#     role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')

# Create your models here.
class User(models.Model):
    ROLE_CHOICES = (
        ('seller', 'Seller'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='user')
    UserId = models.AutoField(primary_key= True)
    UserName = models.CharField(max_length=100) 
    UserEmail = models.EmailField(default='example@example.com') 
    mobileNo = models.CharField(max_length=20) 
    password = models.CharField(max_length=100, default='user') 
    # mobileNo = models.CharField(max_length=100) 
    # mobileNo = models.CharField(max_length=100) 

class Seller(models.Model ):
    ROLE_CHOICES = (
        ('seller', 'Seller'),
        ('user', 'User'),
    )
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default='seller')
    SellerId = models.AutoField(primary_key= True)
    SellerName = models.CharField(max_length=100) 
    SellerEmail = models.EmailField(default='example@example.com') 
    mobileNo = models.CharField(max_length=20) 
    password = models.CharField(max_length=100) 


class UploadedImage(models.Model):
    image = models.ImageField(upload_to='images/')
    uploaded_at = models.DateTimeField(auto_now_add=True)

from django.db import models

class Product(models.Model):
    ProductName = models.CharField(max_length=255)
    Description = models.TextField()
    Category = models.CharField(max_length=255)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    # image = models.CharField(max_length=255)
    image = models.ImageField(upload_to='products/', null=True, blank=True)
    quantity = models.IntegerField(default=1)
    seller = models.ForeignKey(Seller, on_delete=models.CASCADE, default=1)
    productId = models.IntegerField(default=1)

    def __str__(self):
        return self.name
class Cart(models.Model):
    ProductName = models.CharField(max_length=255)
    Description = models.TextField()
    Category = models.CharField(max_length=255)
    Price = models.DecimalField(max_digits=10, decimal_places=2)
    # image = models.CharField(max_length=255)
    image = models.TextField()
    quantity = models.IntegerField(default=1)
    productId = models.IntegerField(default=1)
    user_id = models.IntegerField(default=1)

    # def __str__(self):
    #     return self.name

# class Product(models.Model):
#     name = models.CharField(max_length=100)
#     description = models.TextField()
#     category = models.CharField(max_length=100)
#     price = models.DecimalField(max_digits=8, decimal_places=2)
#     image = models.ImageField(upload_to='products/', null=True, blank=True)