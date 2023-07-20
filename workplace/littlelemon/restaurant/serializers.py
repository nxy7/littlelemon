from rest_framework import serializers
from . import models

class MenuSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Menu
        fields = ['id', 'name', 'price', 'menu_item_description']

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Booking
        fields = '__all__'