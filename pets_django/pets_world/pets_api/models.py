from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    mobile =  models.CharField(max_length=30,null=True)
    address =  models.CharField(max_length=220,null=True)
    location =  models.CharField(max_length=220,null=True)
    role = models.CharField(max_length=220,null=True)
    
   

class UserData(models.Model):
    name = models.CharField(max_length=30,unique=True)
    location = models.CharField(max_length=30)
    about = models.CharField(max_length=30)
    age = models.IntegerField()
    
class Category(models.Model):
    name = models.CharField(max_length=30,default='null')
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)

class PetsData(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='pets')
    age = models.PositiveIntegerField()  # Age in years
    breed = models.CharField(max_length=100)
    description = models.CharField(max_length=225)
    image = models.ImageField(upload_to='pet_images/')
    available = models.BooleanField(default=True)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)

