from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import InscriptionForm, ProfilForm
from .models import EmailVerification
from menu.models import *
from evenements.models import *
from django.db.models import Q
import random
import string



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
    if request.user.is_authenticated:  # Vérifie si l'utilisateur est connecté
        return redirect("profil")
    
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            # Assure-toi qu'il n'y a pas déjà un utilisateur avec cet email
            email = form.cleaned_data["email"]
            if get_user_model().objects.filter(email=email).exists():
                messages.error(request, "Un utilisateur avec cet email existe déjà.")
                return render(request, "utilisateurs/inscription.html", {'form': form})

            user = form.save(commit=False)
            user.is_active = False  # Utilisateur désactivé jusqu'à vérification
            user.save()

            # Génération du code de vérification
            verification_code = ''.join(random.choices(string.digits, k=6))
            
            # Stocker le code dans la base de données
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
    return render(request, 'utilisateurs/inscription.html', {'form': form})


def verifier_email(request, user_id):
    try:
        email_verif = EmailVerification.objects.get(user_id=user_id, is_verified=False)
        print(f"Code de vérification trouvé pour l'utilisateur {user_id}")
    except EmailVerification.DoesNotExist:
        print(f"EmailVerification.DoesNotExist déclenché pour l'utilisateur {user_id}")
        messages.error(request, "Utilisateur ou code introuvable.")
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
            
            messages.success(request, "Email vérifié avec succès ! Vous pouvez maintenant vous connecter.")
            return redirect("connexion")
        else:
            messages.error(request, "Code de vérification incorrect. Réessayez.")
    
    return render(request, "utilisateurs/verifier_email.html", {"email": email_verif.user.email})


def connexion(request):
    if request.user.is_authenticated:  # Vérifie si l'utilisateur est connecté
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
            login(request, user)
            return redirect("profil")
        else:
            messages.error(request, "Identifiant ou mot de passe incorrect.")

    return render(request, "utilisateurs/connexion.html")

def deconnexion(request):
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
                messages.success(request, "Votre profil a été mis à jour avec succès.")
                return redirect("profil")
            else:
                messages.error(request, "Veuillez corriger les erreurs dans le formulaire de profil.")
        elif "password_submit" in request.POST:  # Si le formulaire de mot de passe est soumis
            password_form = PasswordChangeForm(user=user, data=request.POST)
            if password_form.is_valid():
                password_form.save()
                update_session_auth_hash(request, password_form.user)  # Maintient la session active
                messages.success(request, "Votre mot de passe a été modifié avec succès.")
                return redirect("profil")
            else:
                messages.error(request, "Veuillez corriger les erreurs dans le formulaire de mot de passe.")

    return render(request, "utilisateurs/modifier_profil.html", {
        "profil_form": profil_form,
        "password_form": password_form,
    })

@login_required
def ajouter_experience(request):
    user = request.user
    user.ajouter_experience(50)  # Ajoute 50 points d'expérience
    messages.success(request, "Vous avez gagné 50 points d'expérience !")
    return redirect("profil")