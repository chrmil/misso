from django.urls import path
from .views import afficher_historique

urlpatterns = [
    path('historique/', afficher_historique, name='afficher_historique'),
]