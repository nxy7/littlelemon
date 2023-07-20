from django.http import HttpResponse
from django.shortcuts import render
from .forms import BookingForm
from .models import Menu, Booking
import json
from .serializers import BookingSerializer

# Create your views here.
def home(request):
    return render(request, 'index.html')

def about(request):
    return render(request, 'about.html')

def book(request):
    form = BookingForm()
    if request.method == 'POST':
        form = BookingForm(request.POST)
        if form.is_valid():
            form.save()
    context = {'form':form}
    return render(request, 'book.html', context)

# Add your code here to create new views
def menu(request):
    menu_data = Menu.objects.all()
    main_data = {"menu": menu_data}
    return render(request, 'menu.html', main_data)


def reservations(request):
    # menu_data = Menu.objects.all()
    b = Booking.objects.all()
    serialized = BookingSerializer(b, many=True)
    # main_data = {"menu": menu_data}
    return render(request, 'reservations.html', {"bookings": json.dumps(serialized.data)})

def display_menu_items(request, pk=None):
    menu_item = ""
    if pk:
        menu_item = Menu.objects.get(pk=pk)
    return render(request, "menu_item.html", {"menu_item": menu_item})