from django.db import models
from django.conf import settings
from django.utils.timezone import now

class ObjetConnecte(models.Model):
    nom = models.CharField(max_length=100)  # Nom de l'objet
    description = models.TextField(blank=True, null=True)  # Description de l'objet
    niveau_requis = models.PositiveIntegerField(default=1)  # Niveau requis pour modifier l'objet
    actif = models.BooleanField(default=False)  # Statut actif/inactif
    derniere_consultation = models.DateTimeField(blank=True, null=True)  # Dernière consultation
    derniere_utilisation = models.DateTimeField(blank=True, null=True)  # Dernière utilisation
    consommation = models.FloatField(null=False, help_text="Consommation en Watt-heure",) #consommation de l'objet en wh
    consommation_totale = models.FloatField(null=False, default=0,  help_text="Consommation totale de l'objet")

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