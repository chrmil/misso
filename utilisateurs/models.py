from django.contrib.auth.models import AbstractUser
from django.db import models

class Utilisateur(AbstractUser):
    email = models.EmailField(unique=True)  # Empêche les doublons
    date_de_naissance = models.DateField(null=True, blank=True)
    GENRE_CHOIX = [
        ('H', 'Homme'),
        ('F', 'Femme'),
        ('A', 'Autre'),
    ]
    genre = models.CharField(max_length=1, choices=GENRE_CHOIX, null=True, blank=True)

