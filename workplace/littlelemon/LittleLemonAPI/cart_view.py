from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User, UserManager, Group

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.paginator import Paginator, EmptyPage

from rest_framework.decorators import api_view
from restaurant.serializers import MenuSerializer
from restaurant.models import Menu
from .serializers import UserSerializer, CartSerialzier
from .models import Cart

class CartView(APIView):
    def get(self, request):
        u = request.user
        cart = {}
        try:
            cart = Cart.objects.filter(user=u).get()
                        
        except:
            cart = Cart()
            cart.user = u
            cart.save()
        finally:
            serialized = CartSerialzier(cart)
            return Response(serialized.data, status=200)

    def post(self, request, *args, **kwargs):
        itemId = request.data['itemid']

        user: User = request.user
        item = Menu.objects.get(id=itemId)
        cart = Cart.objects.filter(user=user).get()
        cart.items.add(item)
        print(cart)
        cart.save()

        # deliveryGroup = Group.objects.get(name="delivery")
        # deliveryGroup.user_set.add(user)

        return Response("Item added to cart", status=201)

    def delete(self, request):
        user: User = request.user
        cart = Cart.objects.filter(user=user).get()
        cart.items.set([])
        cart.save()


        return Response("Items deleted", status=200)
        
