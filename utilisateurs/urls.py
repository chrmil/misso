from django.urls import path
from .views import *

urlpatterns = [
    path('inscription/', inscription, name='inscription'),
    path('connexion/', connexion, name='connexion'),
    path('deconnexion/', deconnexion, name='deconnexion'),
    path('profil/', profil, name='profil'),
    path('accueil/', accueil, name='accueil'),
    path('hanok/', hanok, name='hanok'),
    path('traiteur/', traiteur, name='traiteur'),
    path('institut/', institut, name='institut'),
    path('terrasse/', terrasse, name='terrasse'),
    path('evenements/', evenements, name='evenements'),
    path('histoire/', histoire, name='histoire'),
]
