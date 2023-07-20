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
from .serializers import UserSerializer, CartSerialzier, OrderSerialzier
from .models import Cart, Order

class OrderView(APIView):
    def get(self, request):
        u = request.user

        orders = []
        try:
            if u.groups.filter(name="manager").exists():
                orders = Order.objects.all()
            elif u.groups.filter(name="delivery").exists():
                orders = Order.objects.filter(deliveryPerson=u).all()
            else:
                orders = Order.objects.filter(user=u).all()
        except:
            return Response([], status=200)

        serialized = OrderSerialzier(orders, many=True)

        return Response(serialized.data, status=200)

    def post(self, request, *args, **kwargs):
        u = request.user
        cart = Cart.objects.filter(user=u).get()
        cartItems = cart.items.all()
        print(cartItems)

        try:
            order = Order(user=u)
            order.save()
            order.items.set(cartItems)
            order.save()
            cart.items.set([])
            cart.save()
            return Response("Done", status=200)
        except Exception as e:
            print(e)
            order.delete()
            return Response(e.__dict__, status=500)

        
class OrderIdView(APIView):
    def get(self, request, *args, **kwargs):
        u = request.user
        oId = kwargs["oId"]
        order = Order.objects.filter(id=oId).get()

        if order.user == u or u.groups.filter(name="manager").exists() or u.groups.filter(name="delivery").exists():
            serialized = OrderSerialzier(order)
            return Response(serialized.data, status=200)
        return Response("Unauthorized", status=403)

    def put(self, request, *args, **kwargs):
        u = request.user
        oId = kwargs["oId"]
        order = Order.objects.filter(id=oId).get()
        if u.groups.filter(name="manager").exists():
            deliveryPersonId = request.data["delivery"]
            dPerson = User.objects.filter(id=deliveryPersonId).get()

            if dPerson.groups.filter(name="delivery").exists == False:
                return Response("Specified person is not part of delivery crew", 500)
                

            order.deliveryPerson = dPerson
            order.save()
            return Response("Done", 200)

        if u.groups.filter(name="delivery").exists() and order.deliveryPerson == u:
            status = request.data["status"]
            order.status = status
            order.save()
            return Response("Done", 200)
        
        return Response("Illegal action", 500)

    def post(self, request, *args, **kwargs):
        u = request.user
        cart = Cart.objects.filter(user=u).get()
        cartItems = cart.items

        order = Order()
        order.user = u
        order.items.set(cartItems)
        order.save()

        cart.items.set([])
        cart.save()

        return Response("Done", status=200)

    def delete(self, request, *args, **kwargs):
        u = request.user
        if u.groups.filter(name="manager").exists() == False:
            return Response("Unauthorized", status=403)

        oId = kwargs["oId"]
        order = Order.objects.filter(id=oId).get()
        order.delete()

        return Response("Done", status=200)
        
