from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import InscriptionForm
from .models import *
from menu.models import *
from django.core.mail import send_mail
from django.conf import settings


def accueil(request):
    return render(request, 'utilisateurs/accueil.html')

def hanok(request):
    restaurant = get_object_or_404(Restaurant, name='hanok')
    categories = Category.objects.filter(restaurant=restaurant)
    menu_items = MenuItem.objects.filter(category__in=categories)
    return render(request, 'utilisateurs/hanok.html' , {'restaurant': restaurant, 'categories': categories, 'menu_items': menu_items})
    

def traiteur(request):
      restaurant = get_object_or_404(Restaurant, name='traiteur')
      categories = Category.objects.filter(restaurant=restaurant)
      menu_items = MenuItem.objects.filter(category__in=categories)
      return render(request, 'utilisateurs/traiteur.html' , {'restaurant': restaurant, 'categories': categories, 'menu_items': menu_items})

def terrasse(request):
    restaurant = get_object_or_404(Restaurant, name='rooftop')
    categories = Category.objects.filter(restaurant=restaurant)
    menu_items = MenuItem.objects.filter(category__in=categories)
    return render(request, 'utilisateurs/terrasse.html', {'restaurant': restaurant, 'categories': categories, 'menu_items': menu_items})

def institut(request):
    return render(request, 'utilisateurs/institut.html')

def evenements(request):
    return render(request, 'utilisateurs/evenements.html')

def histoire(request):
    return render(request, 'utilisateurs/histoire.html')


def inscription(request):
    if request.method == "POST":
        form = InscriptionForm(request.POST)
        if form.is_valid():
            # Sauvegarde l'utilisateur
            user = form.save()

            # Envoi de l'email de confirmation
            send_welcome_email(user.email)

            # Redirige vers la page de connexion
            return redirect('connexion')
    else:
        form = InscriptionForm()

    return render(request, 'utilisateurs/inscription.html', {'form': form})

def send_welcome_email(email):
    subject = 'Bienvenue sur notre site!'
    message = 'Merci de vous être inscrit sur notre site. Nous sommes heureux de vous avoir parmi nous.'
    from_email = settings.EMAIL_HOST_USER  # Ton adresse email définie dans settings.py
    recipient_list = [email]  # L'email de l'utilisateur
    send_mail(subject, message, from_email, recipient_list)

def connexion(request):
    if request.method == "POST":
        identifiant = request.POST['identifiant']  # Peut être email ou username
        password = request.POST['password']
        Utilisateur = get_user_model()

        try:
            user = Utilisateur.objects.get(email=identifiant)
            identifiant = user.username  # On récupère le username associé à l'email
        except Utilisateur.DoesNotExist:
            pass  # Si ce n'est pas un email, Django vérifiera le username

        user = authenticate(request, username=identifiant, password=password)
        if user is not None:
            login(request, user)
            return redirect('profil')
        else:
            return render(request, 'utilisateurs/connexion.html', {'error': "Identifiant ou mot de passe incorrect"})

    return render(request, 'utilisateurs/connexion.html')

def deconnexion(request):
    logout(request)
    return redirect('connexion')

def profil(request):
    return render(request, 'utilisateurs/profil.html', {'user': request.user})
