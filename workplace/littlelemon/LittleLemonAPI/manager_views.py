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

class ManagerApi(APIView):
    def get(self, request):
        if request.user.groups.filter(name='manager').exists() == False:
            return Response("Unauthorized", status=403)
    
        users = User.objects.all()
        managers = []
        for u in users:
            if u.groups.filter(name='manager').exists():
                managers.append(u)    # users.filter(name="nxyt")

        # print(managers)
        serialized = UserSerializer(managers, many=True)

        return Response(serialized.data, status=200)

    def post(self, request ):
        if request.user.groups.filter(name='manager').exists() == False:
            return Response("Unauthorized", status=403)
    
        name = request.data['username']
        user = User.objects.filter(username=name).get()

        managerGroup = Group.objects.get(name="manager")
        managerGroup.user_set.add(user)

        return Response("User added as manager", status=201)

class ManagerWithIdApi(APIView):
    def delete(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists() == False:
            return Response("Unauthorized", status=403)
    
        id = kwargs["uId"]
        user = User.objects.filter(id=id).get()

        managerGroup = Group.objects.get(name="manager")
        managerGroup.user_set.remove(user)

        return Response("Deleted", status=200)

