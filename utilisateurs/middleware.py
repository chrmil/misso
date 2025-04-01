from django.shortcuts import redirect
from django.urls import resolve

class LoginRequiredMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        # Liste des pages accessibles sans connexion
        pages_publiques = ['accueil', 'connexion', 'inscription','histoire','menu','evenements', 'institut','verifier_email']
        #Pour pouvoir accéder au site admin (site protégé par Django)
        if request.path.startswith('/admin/'):
            return self.get_response(request)

        # Vérifie si l'utilisateur essaie d'accéder à une page protégée
        if not request.user.is_authenticated and resolve(request.path_info).url_name not in pages_publiques:
            return redirect('accueil')  # Redirection vers l'accueil

        
        response = self.get_response(request)
        return response
