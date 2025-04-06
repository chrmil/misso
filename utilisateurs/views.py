from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.core.mail import send_mail
from django.conf import settings
from .forms import InscriptionForm, ProfilForm
from .models import EmailVerification
from menu.models import *
from evenements.models import *
from django.db.models import Q
import random
import string
from historique.models import Historique
from historique.utils import enregistrer_historique 
from django.contrib import messages


def institut(request):
    return render(request, 'utilisateurs/institut.html')

def histoire(request):
    return render(request, 'utilisateurs/histoire.html')

def recherche(request):
    plats = Plat.objects.none()
    boissons = Boisson.objects.none()
    plats = Plat.objects.none()
    boissons = Boisson.objects.none()
    restaurants = Restaurant.objects.all()
    categoriesPlats = CategoriePlat.objects.all()
    categoriesBoissons = CategorieBoisson.objects.all()
    accompagnementsPlats = AccompagnementPlat.objects.all()
    accompagnementsBoissons = AccompagnementBoisson.objects.all()

    evenements = Evenement.objects.none()

    if request.method == "POST":
        query = request.POST.get("name")
        type = request.POST.get("type")
        if type != "default":
            nourriture = request.POST.get("nourriture")
            if nourriture != "default":
                categorie = request.POST.get("categorie")
            else:
                categorie = "default"
        else:
            nourriture = "default"
            categorie = "default"

        if type == "default" or type == "nourriture":
            if nourriture == "default" or nourriture == "plat":
                plats = Plat.objects.filter(Q(nom__icontains=query) | Q(description__icontains=query))
                if categorie != "default":
                    plats = plats.filter(categorie=categorie)
                
            if nourriture == "default" or nourriture == "boisson":
                boissons = Boisson.objects.filter(Q(nom__icontains=query) | Q(description__icontains=query))
                if categorie != "default":
                    boissons = boissons.filter(categorie=categorie)

        if type == "default" or type == "événement":
            evenements = Evenement.objects.filter(Q(titre__icontains=query) | Q(description__icontains=query))
    
    else:
        type = "default"
        nourriture = "default"
        categorie = "default"

    return render(request, 'utilisateurs/recherche.html', {'type': type, 
                                                           'nourriture': nourriture,
                                                           'categorie': categorie,
                                                           
                                                           'restaurants': restaurants, 
                                                           'categoriesPlats': categoriesPlats, 
                                                           'categoriesBoissons': categoriesBoissons, 
                                                           'plats': plats, 
                                                           'accompagnementsPlats':accompagnementsPlats, 
                                                           'boissons':boissons, 
                                                           'accompagnementsBoissons':accompagnementsBoissons,
                                                           
                                                           'evenements': evenements})

def inscription(request):
    if request.user.is_authenticated:  # Vérifie si l'utilisateur est déjà connecté
        return redirect("profil")
    
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # Utilisateur désactivé jusqu'à vérification
            user.valide = False  # Compte non validé par défaut
            user.type_personne = form.cleaned_data.get("type_personne")  # Récupère le type de personne
            user.save()

            # Génération du code de vérification
            verification_code = ''.join(random.choices(string.digits, k=6))
            EmailVerification.objects.create(user=user, verification_code=verification_code)

            # Envoi du code de vérification par email
            send_mail(
                subject="Votre code de vérification",
                message=f"Bonjour {user.username},\n\nVotre code de vérification est : {verification_code}\n\nMerci de confirmer votre adresse email.",
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[user.email],
                fail_silently=False,
            )

            messages.success(request, "Inscription réussie ! Un email de vérification vous a été envoyé.")
            return redirect("verifier_email", user_id=user.id)
    else:
        form = InscriptionForm()
    return render(request, "utilisateurs/inscription.html", {'form': form})


def verifier_email(request, user_id):
    try:
        email_verif = EmailVerification.objects.get(user_id=user_id, is_verified=False)
        print(f"Code de vérification trouvé pour l'utilisateur {user_id}")
    except EmailVerification.DoesNotExist:
        print(f"EmailVerification.DoesNotExist déclenché pour l'utilisateur {user_id}")
        return redirect("accueil")

    if request.method == "POST":
        code_saisi = request.POST.get("verification_code")
        if code_saisi == email_verif.verification_code:
            email_verif.is_verified = True
            email_verif.save()

            user = email_verif.user
            user.is_active = True
            user.save()

            email_verif.delete()

            # Enregistrer l'action dans l'historique
            enregistrer_historique(user, "S'est inscrit(e) au système.")
            
            return redirect("connexion")
    
    return render(request, "utilisateurs/verifier_email.html", {"email": email_verif.user.email})


def connexion(request):
    if request.user.is_authenticated:  # Vérifie si l'utilisateur est déjà connecté
        return redirect("profil")

    if request.method == "POST":
        identifiant = request.POST["identifiant"]  # Peut être email ou username
        password = request.POST["password"]
        Utilisateur = get_user_model()

        try:
            user = Utilisateur.objects.get(email=identifiant)
            identifiant = user.username  # Récupérer le username associé
        except Utilisateur.DoesNotExist:
            pass  # Si ce n'est pas un email, Django testera le username

        user = authenticate(request, username=identifiant, password=password)
        if user is not None:
            if not user.valide:  # Vérifie si le compte est validé
                messages.error(request, "Votre compte n'a pas encore été validé par un administrateur.")
                return redirect("connexion")
            login(request, user)
            enregistrer_historique(user, "S'est connecté(e) au système.")
            return redirect("profil")
        else:
            messages.error(request, "Identifiant ou mot de passe incorrect.")

    return render(request, "utilisateurs/connexion.html")

def deconnexion(request):
    if request.user.is_authenticated:
        # Enregistrer l'action dans l'historique
        enregistrer_historique(request.user, "S'est déconnecté(e) du système.")
    logout(request)
    return redirect("connexion")

@login_required
def profil(request):
    user = request.user
    experience_necessaire = user.niveau * 100  # Calcul de l'expérience nécessaire
    progression = int((user.experience / experience_necessaire) * 100)  # Calcul en pourcentage
    return render(request, "utilisateurs/profil.html", {
        "user": user,
        "experience_necessaire": experience_necessaire,
        "progression": progression,
    })

def reservation_page(request):
    return render(request, "utilisateurs/reservation.html")  # Assure-toi d'avoir ce template

def confirmer_reservation(request):
    return render(request, "utilisateurs/confirmation.html")

@login_required
def modifier_profil(request):
    user = request.user
    profil_form = ProfilForm(instance=user)
    password_form = PasswordChangeForm(user=user)

    if request.method == "POST":
        if "profil_submit" in request.POST:  # Si le formulaire de profil est soumis
            profil_form = ProfilForm(request.POST, instance=user)
            if profil_form.is_valid():
                profil_form.save()
                # Enregistrer l'action dans l'historique
                enregistrer_historique(user, "a modifier son profil.")
                return redirect("profil")
            else:
                messages.error(request, "Veuillez corriger les erreurs dans le formulaire de profil.")
        elif "password_submit" in request.POST:  # Si le formulaire de mot de passe est soumis
            password_form = PasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)  # Maintient la session active
                return redirect("profil")


    return render(request, "utilisateurs/modifier_profil.html", {
        "profil_form": profil_form,
        "password_form": password_form,
    })

@login_required
def ajouter_experience(request):
    user = request.user
    user.ajouter_experience(50)  # Ajoute 50 points d'expérience
    return redirect("profil")

def profil_public(request, username):
    Utilisateur = get_user_model()
    utilisateur = get_object_or_404(Utilisateur, username=username)  # Récupère l'utilisateur ou renvoie une 404
    return render(request, "utilisateurs/profil_public.html", {"utilisateur": utilisateur})

def recherche_utilisateurs(request):
    Utilisateur = get_user_model()
    utilisateurs = Utilisateur.objects.none()  # Par défaut, aucun utilisateur n'est affiché

    if request.method == "GET":
        query = request.GET.get("q", "")  # Récupère la requête de recherche
        if query:
            utilisateurs = Utilisateur.objects.filter(username__icontains=query)  # Recherche par nom d'utilisateur

    return render(request, "utilisateurs/recherche_utilisateurs.html", {"utilisateurs": utilisateurs})