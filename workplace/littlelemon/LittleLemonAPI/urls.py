from django.urls import path, include
from . import views, manager_views, delivery_crew_view, cart_view, orders_view, booking_view

urlpatterns = [
    path('menu-items/', views.MenuItemsView.as_view()),
    path('menu-items/<int:menuItemId>', views.MenuItemView.as_view()),
    path('groups/manager/users/', manager_views.ManagerApi.as_view()),
    path('groups/manager/users/<str:uId>', manager_views.ManagerWithIdApi.as_view()),
    path('groups/delivery-crew/users/', delivery_crew_view.DeliveryCrewApi.as_view()),
    path('groups/delivery-crew/users/<str:uId>', delivery_crew_view.DeliveryCrewWithIdAPI.as_view()),
    path('cart/menu-items/', cart_view.CartView.as_view()),
    path('orders/', orders_view.OrderView.as_view()),
    path('categories/', views.CategoryAPI.as_view()),
    path('booking/', booking_view.BookingView.as_view()),
    path('orders/<str:oId>', orders_view.OrderIdView.as_view()),
]
