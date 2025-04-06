from django.db import models
from django.conf import settings

class Historique(models.Model):
    utilisateur = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        default=1  # Remplacez 1 par l'ID d'un utilisateur existant
    )
    date = models.DateTimeField(auto_now_add=True)
    action = models.TextField(default="Action par défaut")

    def __str__(self):
        return f"{self.utilisateur.username} - {self.action} - {self.date}"
