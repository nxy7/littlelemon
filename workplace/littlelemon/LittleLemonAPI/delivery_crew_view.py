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
from .serializers import UserSerializer

class DeliveryCrewApi(APIView):
    def get(self, request):
        if request.user.groups.filter(name='manager').exists() == False:
            return Response("Unauthorized", status=403)
    
        users = User.objects.all()
        delivery = []
        for u in users:
            if u.groups.filter(name='delivery').exists():
                delivery.append(u)    # users.filter(name="nxyt")

        serialized = UserSerializer(delivery, many=True)

        return Response(serialized.data, status=200)

    def post(self, request ):
        if request.user.groups.filter(name='manager').exists() == False:
            return Response("Unauthorized", status=403)
    
        name = request.data['username']
        user = User.objects.filter(username=name).get()

        deliveryGroup = Group.objects.get(name="delivery")
        deliveryGroup.user_set.add(user)

        return Response("User added as delivery crew", status=201)

class DeliveryCrewWithIdAPI(APIView):
    def delete(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists() == False:
            return Response("Unauthorized", status=403)
    
        id = kwargs["uId"]
        user = User.objects.filter(id=id).get()

        deliveryGroup = Group.objects.get(name="delivery")
        deliveryGroup.user_set.remove(user)

        return Response("Deleted", status=200)

