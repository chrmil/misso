from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur  # Remplacez par votre modèle utilisateur

admin.site.register(Utilisateur, UserAdmin)

