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
from historique.utils import enregistrer_historique
from django.http import HttpResponse
from io import BytesIO
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Image
from reportlab.lib.styles import getSampleStyleSheet

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
    plt.figure(figsize=(6, 4))  # Taille réduite
    plt.pie(values_consommation, labels=labels_consommation, autopct='%1.1f%%', startangle=90, colors=["blue", "green", "orange"])
    plt.title("Répartition de la consommation d'énergie")
    buf1 = io.BytesIO()
    plt.savefig(buf1, format='png')
    buf1.seek(0)
    graph1 = base64.b64encode(buf1.read()).decode('utf-8')
    buf1.close()

    # Générer le graphique de quantités (camembert)
    plt.figure(figsize=(6, 4))  # Taille réduite
    plt.pie(values_quantite, labels=labels_quantite, autopct='%1.1f%%', startangle=90, colors=["purple", "cyan", "yellow"])
    plt.title("Répartition du nombre d'objets")
    buf2 = io.BytesIO()
    plt.savefig(buf2, format='png')
    buf2.seek(0)
    graph2 = base64.b64encode(buf2.read()).decode('utf-8')
    buf2.close()

    return render(request, "objets_connectes/rapport_global.html", {"graph1": graph1, "graph2": graph2})


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

    # Enregistrer l'action dans l'historique
    action = f"L'utilisateur {request.user.username} a {'activé' if objet.actif else 'désactivé'} l'objet {objet.nom}."
    enregistrer_historique(request.user, action)
    
    messages.success(request, f"L'objet '{objet.nom}' a été {'activé' if objet.actif else 'désactivé'}.")
    return redirect("liste_objets")

@login_required
def modifier_objet(request, objet_id):
    objet = get_object_or_404(ObjetConnecte, id=objet_id)
    if request.method == "POST":
        # Logique de modification de l'objet
        objet.nom = request.POST.get("nom")
        objet.save()

        # Enregistrer l'action dans l'historique
        action = f"L'utilisateur {request.user.username} a modifié l'objet {objet.nom}."
        enregistrer_historique(request.user, action)

        return redirect("liste_objets")
    return render(request, "objets_connectes/modifier_objet.html", {"objet": objet})

@login_required
def info_objet(request, objet_id):
    objet = get_object_or_404(ObjetConnecte, id=objet_id)
    objet.consulter()  # Met à jour la date de dernière consultation

    # Enregistrer l'action dans l'historique
    action = f"L'utilisateur {request.user.username} a consulté les informations de l'objet {objet.nom}."
    enregistrer_historique(request.user, action)

    return render(request, "objets_connectes/info_objet.html", {"objet": objet})

def telecharger_rapport_pdf(request):
    # Créer un buffer pour le PDF
    buffer = BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=letter)
    styles = getSampleStyleSheet()
    elements = []

    # Ajouter le titre
    elements.append(Paragraph("Rapport Global et Avancé", styles['Title']))
    elements.append(Spacer(1, 12))

    # Ajouter une description
    elements.append(Paragraph("Ce rapport montre la répartition de la consommation d'énergie et du nombre d'objets connectés, ainsi que des statistiques avancées.", styles['BodyText']))
    elements.append(Spacer(1, 12))

    # Ajouter le graphique de consommation
    buf1 = io.BytesIO()
    plt.figure(figsize=(6, 4))
    plt.pie(
        [30, 50, 20],  # Exemple de données
        labels=["Caméras", "Frigos", "Fours"],
        autopct='%1.1f%%',
        startangle=90,
        colors=["blue", "green", "orange"]
    )
    plt.title("Répartition de la consommation d'énergie")
    plt.savefig(buf1, format='png')
    buf1.seek(0)
    elements.append(Image(buf1, width=400, height=300))
    plt.close()  # Fermer la figure pour libérer la mémoire

    elements.append(Spacer(1, 12))

    # Ajouter le graphique de quantités
    buf2 = io.BytesIO()
    plt.figure(figsize=(6, 4))
    plt.pie(
        [40, 35, 25],  # Exemple de données
        labels=["Caméras", "Frigos", "Fours"],
        autopct='%1.1f%%',
        startangle=90,
        colors=["purple", "cyan", "yellow"]
    )
    plt.title("Répartition du nombre d'objets")
    plt.savefig(buf2, format='png')
    buf2.seek(0)
    elements.append(Image(buf2, width=400, height=300))
    plt.close()  # Fermer la figure pour libérer la mémoire

    elements.append(Spacer(1, 12))

    # Ajouter des statistiques avancées
    elements.append(Paragraph("Statistiques avancées :", styles['Heading2']))
    elements.append(Paragraph("1. Consommation totale : 500 kWh", styles['BodyText']))
    elements.append(Paragraph("2. Nombre total d'objets : 120", styles['BodyText']))
    elements.append(Spacer(1, 12))

    # Générer le PDF
    doc.build(elements)

    # Retourner le PDF en tant que réponse HTTP
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')

def telecharger_rapport_avance_pdf(request):
    # Créer un buffer pour le PDF
    buffer = BytesIO()
    p = canvas.Canvas(buffer)

    # Ajouter du contenu détaillé au PDF
    p.drawString(100, 800, "Rapport Avancé")
    p.drawString(100, 780, "Détails sur l'utilisation globale de la plateforme.")
    p.drawString(100, 760, "Inclut des statistiques avancées et des analyses.")
    # Ajoutez ici plus de contenu selon vos besoins

    # Terminer le PDF
    p.showPage()
    p.save()

    # Retourner le PDF en tant que réponse HTTP
    buffer.seek(0)
    return HttpResponse(buffer, content_type='application/pdf')