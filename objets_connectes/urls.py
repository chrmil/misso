from django.urls import path
from .views import *

urlpatterns = [
    path("", liste_objets, name="liste_objets"),
    path("activer/<int:objet_id>/", activer_objet, name="activer_objet"),
    path("modifier/<int:objet_id>/", modifier_objet, name="modifier_objet"),
    path("info/<int:objet_id>/", info_objet, name="info_objet"),  # Nouvelle route pour "Info"
    path("rapport/<int:objet_id>/", rapport_objet, name="rapport_objet"),
    path("rapport_global/", rapport_global, name="rapport_global"),
]