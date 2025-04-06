from django.db import models
from django.utils.timezone import now

class ObjetConnecte(models.Model):
    TYPE_CHOICES = [
        ('camera', 'Caméra'),
        ('frigo', 'Frigo'),
        ('four', 'Four'),
    ]

    nom = models.CharField(max_length=100)  # Nom de l'objet
    description = models.TextField(blank=True, null=True)  # Description de l'objet
    niveau_requis = models.PositiveIntegerField(default=1)  # Niveau requis pour modifier l'objet
    actif = models.BooleanField(default=False)  # Statut actif/inactif
    derniere_consultation = models.DateTimeField(blank=True, null=True)  # Dernière consultation
    derniere_utilisation = models.DateTimeField(blank=True, null=True)  # Dernière utilisation
    consommation = models.FloatField(null=False, help_text="Consommation en Watt-heure")  # Consommation de l'objet en Wh
    type_objet = models.CharField(max_length=10, choices=TYPE_CHOICES, default='camera')  # Type d'objet
    temperature = models.FloatField(blank=True, null=True, help_text="Température en °C (uniquement pour frigo et four)")  # Température
    nombre_consultations = models.PositiveIntegerField(default=0, help_text="Nombre total de consultations")  # Nombre total de consultations

    def consulter(self):
        """Met à jour la date de dernière consultation et incrémente le compteur."""
        self.derniere_consultation = now()
        self.nombre_consultations += 1
        self.save()

    def utiliser(self):
        """Met à jour la date de dernière utilisation."""
        self.derniere_utilisation = now()
        self.save()

    def __str__(self):
        return self.nom

    def save(self, *args, **kwargs):
        """Personnalise la sauvegarde pour gérer les champs spécifiques au type."""
        if self.type_objet == 'camera':
            self.temperature = None  # Supprime la température si c'est une caméra
        super().save(*args, **kwargs)