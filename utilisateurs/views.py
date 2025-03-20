from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout, get_user_model
from .forms import InscriptionForm

def accueil(request):
    return render(request, 'utilisateurs/accueil.html')

def hanok(request):
    return render(request, 'utilisateurs/hanok.html')

def traiteur(request):
    return render(request, 'utilisateurs/traiteur.html')

def terrasse(request):
    return render(request, 'utilisateurs/terrasse.html')

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
            form.save()
            return redirect('connexion')
    else:
        form = InscriptionForm()
    return render(request, 'utilisateurs/inscription.html', {'form': form})

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
