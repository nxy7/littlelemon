from django.db import models
import datetime


# Create your models here.
class Booking(models.Model):
   first_name = models.CharField(max_length=200)    
   last_name = models.CharField(max_length=200)

   reservation_date = models.DateField()
   reservation_slot = models.SmallIntegerField(default=10)

   comment = models.CharField(max_length=1000)

   def __str__(self):
      return self.first_name + ' ' + self.last_name
      
class Category(models.Model):
   name = models.CharField(max_length=100)

class Menu(models.Model):
   name = models.CharField(max_length=200)
   price = models.IntegerField()
   menu_item_description = models.TextField(max_length=1000, default='')
   categories = models.ManyToManyField(Category)

   def __str__(self):
      return self.name


# Add code to create Menu model