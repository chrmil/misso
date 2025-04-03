from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import ObjetConnecte

@login_required
def liste_objets(request):
    objets = request.user.objets_connectes.all()
    return render(request, "objets_connectes/liste_objets.html", {"objets": objets})

@login_required
def activer_objet(request, objet_id):
    objet = get_object_or_404(ObjetConnecte, id=objet_id, utilisateur=request.user)
    objet.actif = not objet.actif
    objet.save()
    messages.success(request, f"L'objet '{objet.nom}' a été {'activé' if objet.actif else 'désactivé'}.")
    return redirect("liste_objets")

@login_required
def modifier_objet(request, objet_id):
    objet = get_object_or_404(ObjetConnecte, id=objet_id, utilisateur=request.user)
    if request.user.niveau < objet.niveau_requis:
        messages.error(request, f"Vous devez être au niveau {objet.niveau_requis} pour modifier cet objet.")
        return redirect("liste_objets")
    if request.method == "POST":
        objet.nom = request.POST.get("nom", objet.nom)
        objet.description = request.POST.get("description", objet.description)
        objet.save()
        messages.success(request, f"L'objet '{objet.nom}' a été modifié.")
        return redirect("liste_objets")
    return render(request, "objets_connectes/modifier_objet.html", {"objet": objet})