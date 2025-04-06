from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import Utilisateur

class UtilisateurAdmin(UserAdmin):
    # Champs affichés dans la liste des utilisateurs
    list_display = ('username', 'email', 'valide', 'niveau', 'experience', 'type_personne', 'is_active', 'is_staff')
    # Champs modifiables via des filtres
    list_filter = ('valide', 'type_personne', 'is_active', 'is_staff')
    # Champs modifiables dans le formulaire d'édition
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('valide', 'niveau', 'experience', 'type_personne')}),  # Ajout des champs personnalisés
    )
    # Champs disponibles lors de la création d'un utilisateur
    add_fieldsets = UserAdmin.add_fieldsets + (
        (None, {'fields': ('valide', 'niveau', 'experience', 'type_personne')}),  # Ajout des champs personnalisés
    )

admin.site.register(Utilisateur, UtilisateurAdmin)