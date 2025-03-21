from django.shortcuts import render, redirect, get_object_or_404
from .models import *



def menu(request, restaurant_name):
    restaurant = get_object_or_404(Restaurant, name=restaurant_name)
    categories = Category.objects.filter(restaurant=restaurant)
    menu_items = MenuItem.objects.filter(category__in=categories)
    return render(request, 'menu', {'restaurant': restaurant, 'categories': categories, 'menu_items': menu_items})

