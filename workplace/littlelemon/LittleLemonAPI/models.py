from django.db import models
from restaurant.models import Menu
from django.contrib.auth.models import User, UserManager, Group

class Cart(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    items = models.ManyToManyField(Menu, serialize=True)

class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    deliveryPerson = models.ForeignKey(User, on_delete=models.CASCADE, related_name="delivery", null=True)
    status = models.IntegerField(default=0)
    items = models.ManyToManyField(Menu, serialize=True)

