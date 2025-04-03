from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import ObjetConnecte

@login_required
def liste_objets(request):
    user = request.user
    user.ajouter_experience(50)  # Ajoute 50 points d'expérience
    objets = ObjetConnecte.objects.all()  # Récupère tous les objets connectés
    return render(request, "objets_connectes/liste_objets.html", {"objets": objets})

@login_required
def activer_objet(request, objet_id):
    objet = get_object_or_404(ObjetConnecte, id=objet_id)
    objet.actif = not objet.actif
    objet.utiliser()  # Met à jour la date de dernière consultation
    objet.save()
    return redirect("liste_objets")

@login_required
def modifier_objet(request, objet_id):
    objet = get_object_or_404(ObjetConnecte, id=objet_id)
    if request.user.niveau < objet.niveau_requis:
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