from django.urls import path
from .views import (
    inscription, connexion, deconnexion, profil, accueil,
    hanok, traiteur, institut, terrasse, evenements,
    histoire, verifier_email,reservation_page, confirmer_reservation
)

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
    path('histoire/', histoire, name='histoire'),
    path('verifier_email/<int:user_id>/', verifier_email, name='verifier_email'),  # Ajout du paramètre user_id
    path("reservation/", reservation_page, name="reservation"),
    path("confirmer_reservation/", confirmer_reservation, name="confirmer_reservation"),
]
