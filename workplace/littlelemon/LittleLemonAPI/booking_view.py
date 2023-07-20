from django.shortcuts import render
from django.http import HttpResponse
from django.views import View
from django.contrib.auth.models import User, UserManager, Group
from django.shortcuts import redirect

from rest_framework.renderers import JSONRenderer
from rest_framework.response import Response
from rest_framework.views import APIView

from django.core.paginator import Paginator, EmptyPage

from rest_framework.decorators import api_view
from restaurant.serializers import MenuSerializer, BookingSerializer
from restaurant.models import Booking
from .serializers import UserSerializer
import datetime


class BookingView(APIView):
    def get(self, request, *args, **kwargs):
        date = request.query_params.get("date")
        b = {}
        if date:
            print(date)
            b = Booking.objects.filter(reservation_date=date).all()
        else:
            b = Booking.objects.all()
        serialized = BookingSerializer(b, many=True)

        return Response(serialized.data, status=200)

    def post(self, request):
        user: User = request.user

        bs = BookingSerializer(data=request.data)
        if bs.is_valid():
            # print(bs.validated_data["reservation_date"])
            if Booking.objects.filter(reservation_date=bs.validated_data["reservation_date"], reservation_slot=bs.validated_data["reservation_slot"]).exists():
                return Response("Date is already taken", status=400)

            bs.save()

            return Response(bs.data, status=201)
        else:
            return Response("Error", status=500)
