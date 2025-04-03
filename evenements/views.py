import random
import string
from django.shortcuts import redirect, render
from django.utils import timezone
from django.views.generic.detail import DetailView
from evenements.forms import EvenementForm
from evenements.models import Evenement
from django.views.generic.dates import *
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django import forms
from django.contrib.auth.forms import UserCreationForm
from utilisateurs.models import EmailVerification, Utilisateur
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib import messages
from django.core.mail import send_mail


class EvenementArchiveIndexView(ArchiveIndexView):
    model = Evenement
    queryset = Evenement.objects.all()
    date_field = "date"
    allow_future = True


class EvenementDetailView(DetailView):
    model = Evenement
    template = "evenement_detail.html"
    context_objet_name="evenement"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        slug = self.kwargs.get('slug')
        return context
    
@login_required(redirect_field_name="connexion")
def demande_evenement(request):
    if not (request.user.is_authenticated):  # Vérifie si l'utilisateur n'est pas connecté
        return redirect("connexion")
    if request.method == "POST":
        form = EvenementForm(request.POST)
        if form.is_valid():
            # Récupère l'email de l'utilisateur
            user=request.user
            email = user.email
            evenement = form.save(commit=False)
            evenement.email=email
            evenement.etat = False  # Demande désactivée jusqu'à vérification
            evenement.save()
            messages.success(request, "Votre demande a été envoyée.")
            return redirect("vos_evenements")
    else:
        form = EvenementForm()
    return render(request, 'evenements/evenement_form.html', {'form': form})



@login_required(redirect_field_name="connexion")
def voir_demande(request):
    user = request.user
    demandes = Evenement.objects.filter(email=user.email)
    return render(request, 'evenements/evenement_demande.html', { 'demandes': demandes})
