from django.shortcuts import render, redirect, get_object_or_404
from .models import *



def menu(request,restaurant_nom):
    restaurant = get_object_or_404(Restaurant, nom=restaurant_nom)
    menus = Menu.objects.filter(restaurant=restaurant)
    categoriesPlats = CategoriePlat.objects.all()
    categoriesBoissons= CategorieBoisson.objects.all()
    plats = Plat.objects.filter(categorie__in=categoriesPlats, menu__in=menus)
    accompagnementsPlats = AccompagnementPlat.objects.filter(plat__in=plats)
    boissons = Boisson.objects.filter(categorie__in=categoriesBoissons, menu__in=menus)
    accompagnementsBoissons = AccompagnementBoisson.objects.filter(boisson__in=boissons)
    return render(request, 'menu/restaurant.html', { 'restaurant': restaurant,'menus': menus, 'categoriesPlats': categoriesPlats, 'plats': plats, 'accompagnementsPlats':accompagnementsPlats,'boissons':boissons,'accompagnementsBoissons':accompagnementsBoissons})
