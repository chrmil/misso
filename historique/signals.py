from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import Historique
from objets_connectes.models import ObjetConnecte
from django.conf import settings

@receiver(post_save, sender=ObjetConnecte)
def enregistrer_modification_objet(sender, instance, created, **kwargs):
    utilisateur = getattr(instance, 'modifie_par', None)  # Si vous avez un champ pour l'utilisateur
    if utilisateur:
        action = f"L'objet {instance.nom} a été {'créé' if created else 'modifié'}."
        Historique.objects.create(utilisateur=utilisateur, action=action)

@receiver(post_delete, sender=ObjetConnecte)
def enregistrer_suppression_objet(sender, instance, **kwargs):
    utilisateur = getattr(instance, 'modifie_par', None)
    if utilisateur:
        action = f"L'objet {instance.nom} a été supprimé."
        Historique.objects.create(utilisateur=utilisateur, action=action)