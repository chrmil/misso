from django.contrib import admin
from .models import Historique

class HistoriqueAdmin(admin.ModelAdmin):
    list_display = ('utilisateur', 'action', 'date')  # Colonnes affichées
    list_filter = ('date', 'utilisateur')  # Filtres dans l'admin
    search_fields = ('utilisateur__username', 'action')  # Barre de recherche

admin.site.register(Historique, HistoriqueAdmin)
