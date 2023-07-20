from django.shortcuts import render
from django.http import HttpResponse
from django.views import View

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.paginator import Paginator, EmptyPage

from rest_framework.decorators import api_view
from restaurant.serializers import MenuSerializer
from .serializers import CategorySerialzier
# from rest_framework.permissions import IsAdminUser


from restaurant import models

# Create your views here.
def hello(request):
    return HttpResponse("elo")



class MenuItemsView(APIView):
    # renderer_classes = [JSONRenderer]
    
    def get(self, request, *args, **kwargs):
        per_page = request.query_params.get("per_page", default=5)
        page = request.query_params.get("page", default=1)
        menu_items = models.Menu.objects.all()

        pagiator = Paginator(menu_items, per_page=per_page)
        try:
            menu_items = pagiator.page(number=page)
        except:
            menu_items=[]

        resp = MenuSerializer(menu_items, many=True)
        
        return Response(resp.data)
        
    def put(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists() == False:
            return Response("Unauthorized", status=403)

        serializer = MenuSerializer(data=request.data)
        id = ""
        try:
            id = request.data["id"]
        except:
            return Response("You need to pass ID in order to update object", status=404)

        if serializer.is_valid():
            m = models.Menu.objects.get(id=id)
            m.name = serializer.data["name"]
            m.price = serializer.data["price"]
            m.menu_item_description = serializer.data["menu_item_description"]
            m.save()

            serialized = MenuSerializer(data=m.__dict__)
            if serialized.is_valid():
                return Response(serialized.data, status=200)
            else:
                return Response(serialized.errors, status=500)
            

        return Response("Invalid data format", status=500)
        

    def post(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists() == False:
            return Response("Unauthorized", status=403)

        serializer = MenuSerializer(data=request.data)
        if serializer.is_valid():
            item: models.Menu = serializer.save()
            item.save()
            return Response(serializer.data, status=201)
        
        return Response("Invalid data format", status=500)

        

    def patch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists() == False:
            return Response("Unauthorized", status=403)

        return Response("Unauthorized", status=403)

    def delete(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists() == False:
            return Response("Unauthorized", status=403)
        
        try:
            id = request.data["id"]

            models.Menu.objects.filter(id=id).delete()
            return Response("Done", status=200)        
        except Exception as e:
            print(e)
            return Response(e.__dict__, status=500)        


class MenuItemView(APIView):
    def get(self, request, *args, **kwargs):
        pathParam = kwargs["menuItemId"]
        item = models.Menu.objects.get(id=pathParam)
        
        return Response(MenuSerializer(item).data)
        
    def put(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists() == False:
            return Response("Unauthorized", status=403)
        id = kwargs["menuItemId"]
        serializer = MenuSerializer(data=request.data)

        if serializer.is_valid():
            m = models.Menu.objects.get(id=id)
            m.name = serializer.data["name"]
            m.price = serializer.data["price"]
            m.menu_item_description = serializer.data["menu_item_description"]
            m.save()

            serialized = MenuSerializer(data=m.__dict__)
            if serialized.is_valid():
                return Response(serialized.data, status=200)
            else:
                return Response(serialized.errors, status=500)
            

        return Response("Invalid data format", status=500)

    def patch(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists() == False:
            return Response("Unauthorized", status=403)
        id = kwargs["menuItemId"]
        serializer = MenuSerializer(data=request.data)

        if serializer.is_valid():
            m = models.Menu.objects.get(id=id)
            m.name = serializer.data["name"]
            m.price = serializer.data["price"]
            m.menu_item_description = serializer.data["menu_item_description"]
            m.save()

            serialized = MenuSerializer(data=m.__dict__)
            if serialized.is_valid():
                return Response(serialized.data, status=200)
            else:
                return Response(serialized.errors, status=500)
            

        return Response("Invalid data format", status=500)

    def delete(self, request, *args, **kwargs):
        if request.user.groups.filter(name='manager').exists() == False:
            return Response("Unauthorized", status=403)

        id = kwargs["menuItemId"]
        models.Menu.objects.filter(id=id).delete()
        return Response("Done", status=200)        

class Cart(APIView):
    def get(self, request, *args, **kwargs):
        pathParam = kwargs["menuItemId"]
        item = models.Menu.objects.get(id=pathParam)
        
        return Response(MenuSerializer(item).data)

class CategoryAPI(APIView):
    def get(self, request, *args, **kwargs):
        m = models.Category.objects.all()
        serialized = CategorySerialzier(m, many=True)

        return Response(serialized.data, status=200)

    def post(self, request, *args, **kwargs): 
        if request.user.groups.filter(name='manager').exists() == False:
            return Response("Unauthorized", status=403)
        name = request.data["name"]
        newCategory = models.Category()
        newCategory.name = name
        newCategory.save()
        # data = request.data

        return Response("Ok", status=200)
