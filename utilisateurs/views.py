from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .forms import InscriptionForm, ProfilForm
from .models import EmailVerification
from menu.models import *
import random
import string

def accueil(request):
    return render(request, 'utilisateurs/accueil.html')



def institut(request):
    return render(request, 'utilisateurs/institut.html')

def histoire(request):
    return render(request, 'utilisateurs/histoire.html')


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

    # Vérification si un code est déjà saisi et si la méthode est POST
    if request.method == "POST":
        code_saisi = request.POST.get("verification_code")
        if code_saisi == email_verif.verification_code:
            email_verif.is_verified = True
            email_verif.save()

            # Activer le compte utilisateur
            user = email_verif.user
            user.is_active = True
            user.save()

            # Supprimer l'entrée de la table EmailVerification
            email_verif.delete()
            
            messages.success(request, "Email vérifié avec succès ! Vous pouvez maintenant vous connecter.")
            return redirect("connexion")
        else:
            messages.error(request, "Code de vérification incorrect. Réessayez.")
    
    # La page d'affichage si ce n'est pas un POST (juste un GET)
    return render(request, "utilisateurs/verifier_email.html", {"user_id": user_id})


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

def profil(request):
    return render(request, "utilisateurs/profil.html", {"user": request.user})

def reservation_page(request):
    return render(request, "utilisateurs/reservation.html")  # Assure-toi d'avoir ce template

def confirmer_reservation(request):
    return render(request, "utilisateurs/confirmation.html")

@login_required
def modifier_profil(request):
    user = request.user
    if request.method == "POST":
        form = ProfilForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, "Votre profil a été mis à jour avec succès.")
            return redirect("profil")
        else:
            messages.error(request, "Veuillez corriger les erreurs ci-dessous.")
    else:
        form = ProfilForm(instance=user)
    return render(request, "utilisateurs/modifier_profil.html", {"form": form})