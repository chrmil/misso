from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings




class Utilisateur(AbstractUser):
    email = models.EmailField(unique=True)  # Empêche les doublons
    date_de_naissance = models.DateField(null=True, blank=True)
    GENRE_CHOIX = [
        ('H', 'Homme'),
        ('F', 'Femme'),
        ('A', 'Autre'),
    ]
    genre = models.CharField(max_length=1, choices=GENRE_CHOIX, null=True, blank=True)

class EmailVerification(models.Model):
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)  # Ajoute ce champ




