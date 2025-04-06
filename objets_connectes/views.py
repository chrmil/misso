from datetime import date, datetime, timedelta, timezone
from datetime import time
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ObjetConnecte
from django.utils import timezone


@login_required
def liste_objets(request):
    user = request.user
    user.ajouter_experience(50)  # Ajoute 50 points d'expérience
    objets = ObjetConnecte.objects.all()  # Récupère tous les objets connectés
    return render(request, "objets_connectes/liste_objets.html", {"objets": objets})

@login_required
def activer_objet(request, objet_id):
    objet = get_object_or_404(ObjetConnecte, id=objet_id)
    
    # Vérifie si l'utilisateur a le niveau requis
    if request.user.niveau < objet.niveau_requis:
        messages.error(request, "Vous n'avez pas le niveau requis pour activer cet objet.", extra_tags=str(objet.id))
        return redirect("liste_objets")
    
    # Alterne le statut actif/inactif de l'objet
    objet.actif = not objet.actif

    objet.utiliser()  # Met à jour la date de dernière consultation
    if(not(objet.actif)):
        objet.consommation_totale = objet.consommation_totale+((timezone.now()-objet.derniere_utilisation).total_seconds()/360)*objet.consommation

    objet.save()
    
    messages.success(request, f"L'objet '{objet.nom}' a été {'activé' if objet.actif else 'désactivé'}.", extra_tags=str(objet.id))
    return redirect("liste_objets")

@login_required
def modifier_objet(request, objet_id):
    objet = get_object_or_404(ObjetConnecte, id=objet_id)
    if request.user.niveau < 10:
        return redirect("liste_objets")
    if request.method == "POST":
        objet.nom = request.POST.get("nom", objet.nom)
        objet.description = request.POST.get("description", objet.description)
        objet.utiliser()
        objet.save()
        return redirect("liste_objets")
    return render(request, "objets_connectes/modifier_objet.html", {"objet": objet})

@login_required
def info_objet(request, objet_id):
    objet = get_object_or_404(ObjetConnecte, id=objet_id)
    objet.consulter()  # Met à jour la date de dernière consultation
    return render(request, "objets_connectes/info_objet.html", {"objet": objet})