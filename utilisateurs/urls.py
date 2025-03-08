from django.urls import path
from .views import inscription, connexion, deconnexion, profil, accueil

urlpatterns = [
    path('inscription/', inscription, name='inscription'),
    path('connexion/', connexion, name='connexion'),
    path('deconnexion/', deconnexion, name='deconnexion'),
    path('profil/', profil, name='profil'),
    path('accueil/', accueil, name='accueil'),
]
