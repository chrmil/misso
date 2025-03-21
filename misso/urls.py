from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect

urlpatterns = [
    path('menu/', include('menu.urls')),
    path('admin/', admin.site.urls),
    path('', include('utilisateurs.urls')),
    path('', lambda request: redirect('accueil/', permanent=False)),
]
