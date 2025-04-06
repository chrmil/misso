from django.db import models
from django.contrib.auth import get_user_model

Utilisateur = get_user_model()

class Historique(models.Model):
    utilisateur = models.ForeignKey(Utilisateur, on_delete=models.CASCADE, related_name="historiques")
    action = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.utilisateur.username} - {self.action} - {self.date}"