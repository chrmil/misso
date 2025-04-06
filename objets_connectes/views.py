from datetime import date, datetime, timedelta, timezone
from datetime import time
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ObjetConnecte
from django.db.models import Sum
from django.utils import timezone
import matplotlib.pyplot as plt
import io
import urllib, base64

def rapport_global(request):
    # Calculer la consommation totale par type d'objet
    consommation_par_type = {
        "Caméras": ObjetConnecte.objects.filter(type_objet="camera").aggregate(Sum("consommation"))["consommation__sum"] or 0,
        "Frigos": ObjetConnecte.objects.filter(type_objet="frigo").aggregate(Sum("consommation"))["consommation__sum"] or 0,
        "Fours": ObjetConnecte.objects.filter(type_objet="four").aggregate(Sum("consommation"))["consommation__sum"] or 0,
    }

    # Calculer le nombre total d'objets par type
    quantite_par_type = {
        "Caméras": ObjetConnecte.objects.filter(type_objet="camera").count(),
        "Frigos": ObjetConnecte.objects.filter(type_objet="frigo").count(),
        "Fours": ObjetConnecte.objects.filter(type_objet="four").count(),
    }

    # Préparer les données pour le graphique de consommation
    labels_consommation = consommation_par_type.keys()
    values_consommation = consommation_par_type.values()

    # Préparer les données pour le graphique de quantités
    labels_quantite = quantite_par_type.keys()
    values_quantite = quantite_par_type.values()

    # Générer le graphique de consommation (camembert)
    plt.figure(figsize=(12, 6))
    plt.subplot(1, 2, 1)  # Premier graphique
    plt.pie(values_consommation, labels=labels_consommation, autopct='%1.1f%%', startangle=90, colors=["blue", "green", "orange"])
    plt.title("Répartition de la consommation d'énergie")

    # Générer le graphique de quantités (camembert)
    plt.subplot(1, 2, 2)  # Deuxième graphique
    plt.pie(values_quantite, labels=labels_quantite, autopct='%1.1f%%', startangle=90, colors=["purple", "cyan", "yellow"])
    plt.title("Répartition du nombre d'objets")

    # Convertir les graphiques en image pour l'afficher dans le template
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    buf.close()

    return render(request, "objets_connectes/rapport_global.html", {"graph": uri})


def rapport_objet(request, objet_id):
    objet = get_object_or_404(ObjetConnecte, id=objet_id)

    # Exemple de données pour le graphique (vous pouvez personnaliser selon vos besoins)
    labels = ['Consultations', 'Utilisations']
    values = [
        (objet.derniere_consultation - objet.derniere_utilisation).total_seconds() / 3600 if objet.derniere_consultation and objet.derniere_utilisation else 0,
        objet.consommation
    ]

    # Générer un graphique avec Matplotlib
    plt.figure(figsize=(6, 4))
    plt.bar(labels, values, color=['blue', 'green'])
    plt.title(f"Statistiques pour {objet.nom}")
    plt.ylabel("Valeurs")
    plt.xlabel("Catégories")

    # Convertir le graphique en image pour l'afficher dans le template
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    string = base64.b64encode(buf.read())
    uri = urllib.parse.quote(string)
    buf.close()

    return render(request, "objets_connectes/rapport_objet.html", {"objet": objet, "graph": uri})


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
        messages.error(request, "Vous n'avez pas le niveau requis pour activer cet objet.")
        return redirect("liste_objets")
    
    # Alterne le statut actif/inactif de l'objet
    objet.actif = not objet.actif
    objet.utiliser()  # Met à jour la date de dernière utilisation
    objet.save()
    
    messages.success(request, f"L'objet '{objet.nom}' a été {'activé' if objet.actif else 'désactivé'}.")
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