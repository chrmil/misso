from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from .models import Historique

@login_required
def afficher_historique(request):
    historique = Historique.objects.filter(utilisateur=request.user).order_by('-date')
    return render(request, 'historique/historique.html', {'historique': historique})
