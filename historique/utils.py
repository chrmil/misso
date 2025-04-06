from .models import Historique

def enregistrer_historique(utilisateur, action):
    """
    Enregistre une action dans l'historique.
    :param utilisateur: L'utilisateur qui a effectué l'action.
    :param action: Une description de l'action effectuée.
    """
    Historique.objects.create(utilisateur=utilisateur, action=action)