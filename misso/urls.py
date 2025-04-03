from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('restaurants/', include('menu.urls')),
    path('admin/', admin.site.urls),
    path('', include('utilisateurs.urls')),
    path('evenements/',include('evenements.urls')),
    path('', lambda request: redirect('accueil/', permanent=False)),
    path("objets_connectes/", include("objets_connectes.urls")),
]
