from django.contrib import admin
from .models import *

admin.site.register(ObjetConnecte)
readonly_fields = [ObjetConnecte.consommation_totale]