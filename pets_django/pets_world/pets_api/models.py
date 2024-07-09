from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

class CustomUser(AbstractUser):
    mobile =  models.CharField(max_length=30,null=True)
    address =  models.CharField(max_length=220,null=True)
    location =  models.CharField(max_length=220,null=True)
    role = models.CharField(max_length=220,null=True)
    
       
class Category(models.Model):
    name = models.CharField(max_length=30,default='null')
    image = models.ImageField(upload_to='category_images/', blank=True, null=True)


class PetDetails(models.Model):
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='pets')
    donor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='donor', null=True, blank=True)
    age = models.CharField(max_length=100, default='')  
    breed = models.CharField(max_length=100, default='')
    description = models.CharField(max_length=500, default='')
    image = models.ImageField(upload_to='pet_images/', default='')
    available = models.BooleanField(default=False)
    date_added = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)

class AdoptedPets(models.Model):
    pet = models.ForeignKey(PetDetails, on_delete=models.CASCADE, related_name='pet')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user', null=True, blank=True)
    date_adopted = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(default=0)

class AdoptionNotification(models.Model):
    pet = models.ForeignKey(PetDetails, on_delete=models.CASCADE, related_name='pett')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='userr', null=True, blank=True)
    message = models.CharField(max_length=225, default='')
    status = models.IntegerField(default=0)





