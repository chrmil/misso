from django.db import models
from django.conf import settings
from django.utils.timezone import now

class ObjetConnecte(models.Model):
    id = models.AutoField(primary_key=True)
    nom = models.CharField(max_length=100)  # Nom de l'objet
    description = models.TextField(blank=True, null=True)  # Description de l'objet
    niveau_requis = models.PositiveIntegerField(default=1)  # Niveau requis pour modifier l'objet
    actif = models.BooleanField(default=False)  # Statut actif/inactif
    derniere_consultation = models.DateTimeField(blank=True, null=True)  # Dernière consultation
    derniere_utilisation = models.DateTimeField(blank=True, null=True)  # Dernière utilisation

    def consulter(self):
        """Met à jour la date de dernière consultation."""
        self.derniere_consultation = now()
        self.save()

    def utiliser(self):
        """Met à jour la date de dernière utilisation."""
        self.derniere_utilisation = now()
        self.save()

    def __str__(self):
        return self.nom