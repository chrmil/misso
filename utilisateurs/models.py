from django.contrib.auth.models import AbstractUser
from django.db import models
from django.conf import settings
from django.contrib.auth.models import Group



class Utilisateur(AbstractUser):
    email = models.EmailField(unique=True)  # Empêche les doublons
    date_de_naissance = models.DateField(null=True, blank=True)
    GENRE_CHOIX = [
        ('H', 'Homme'),
        ('F', 'Femme'),
        ('A', 'Autre'),
    ]
    genre = models.CharField(max_length=1, choices=GENRE_CHOIX, null=True, blank=True)
    niveau = models.PositiveIntegerField(default=1)  # Niveau de l'utilisateur
    experience = models.PositiveIntegerField(default=0)  # Points d'expérience de l'utilisateur

    def ajouter_experience(self, points):
        """Ajoute des points d'expérience et gère le passage au niveau supérieur."""
        self.experience += points
        while self.experience >= self.experience_necessaire():
            self.experience -= self.experience_necessaire()
            self.niveau += 1
        if(self.niveau>=10):
           self.is_staff=True
           mon_groupe = Group.objects.get(name='Modérateurs') 
           mon_groupe.user_set.add(self)
        self.save()

    def experience_necessaire(self):
        """Calcule l'expérience nécessaire pour passer au niveau suivant."""
        return self.niveau * 100  # Exemple : 100 points par niveau

   



class EmailVerification(models.Model):
    user = models.ForeignKey(Utilisateur, on_delete=models.CASCADE)
    verification_code = models.CharField(max_length=6, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_verified = models.BooleanField(default=False)  # Ajoute ce champ


