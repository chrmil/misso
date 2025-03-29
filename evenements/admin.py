from django.contrib import admin
from evenements.models import *

class EvenementAdmin(admin.ModelAdmin):
  list_display = ("titre", "date", "description",)
  prepopulated_fields = {"slug": ("date", "titre")}
  readonly_fields = ("slug")

admin.site.register(Evenement)

