from django.contrib.auth.models import User, UserManager
from rest_framework import serializers
from .models import Cart
from restaurant.models import Category
from restaurant.serializers import MenuSerializer


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id','username', 'email']

class CartSerialzier(serializers.ModelSerializer):
    # category_name = serializers.ReadOnlyField(source='items.price')
    items = MenuSerializer(read_only=True, many=True)
    class Meta:
        model = Cart
        fields = ['items']

class OrderSerialzier(serializers.ModelSerializer):
    # category_name = serializers.ReadOnlyField(source='items.price')
    user = UserSerializer(read_only=True)
    deliveryPerson = UserSerializer(read_only=True)
    items = MenuSerializer(read_only=True, many=True)
    class Meta:
        model = Cart
        fields = '__all__'

class CategorySerialzier(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields='__all__'