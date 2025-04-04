from django.urls import path
from .views import *

urlpatterns = [
    path('inscription/', inscription, name='inscription'),
    path('connexion/', connexion, name='connexion'),
    path('deconnexion/', deconnexion, name='deconnexion'),
    path('profil/', profil, name='profil'),
    path('institut/', institut, name='institut'),
    path('histoire/', histoire, name='histoire'),
    path('recherche/', recherche, name='recherche'),
    path('verifier_email/<int:user_id>/', verifier_email, name='verifier_email'),  # Ajout du paramètre user_id
    path("reservation/", reservation_page, name="reservation"),
    path("confirmer_reservation/", confirmer_reservation, name="confirmer_reservation"),
    path('modifier_profil/', modifier_profil, name='modifier_profil'),
    path('ajouter_experience/', ajouter_experience, name='ajouter_experience'),
]
