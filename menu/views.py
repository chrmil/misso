from django.shortcuts import render, redirect, get_object_or_404
from .models import *



def menu(request,restaurant_nom):
    restaurant = get_object_or_404(Restaurant, nom=restaurant_nom)
    menus = Menu.objects.filter(restaurant=restaurant).order_by("priorite")
    categoriesPlats = CategoriePlat.objects.all().order_by("priorite")
    categoriesBoissons= CategorieBoisson.objects.all().order_by("priorite")
    plats = Plat.objects.filter(categorie__in=categoriesPlats, menu__in=menus).order_by("priorite")
    accompagnementsPlats = AccompagnementPlat.objects.filter(plat__in=plats).order_by("priorite")
    boissons = Boisson.objects.filter(categorie__in=categoriesBoissons, menu__in=menus).order_by("priorite")
    accompagnementsBoissons = AccompagnementBoisson.objects.filter(boisson__in=boissons).order_by("priorite")
    return render(request, 'menu/restaurant.html', { 'restaurant': restaurant,'menus': menus, 'categoriesPlats': categoriesPlats, 'plats': plats, 'accompagnementsPlats':accompagnementsPlats, 'categoriesBoissons': categoriesBoissons, 'boissons':boissons,'accompagnementsBoissons':accompagnementsBoissons})
