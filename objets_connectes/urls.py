from django.urls import path
from .views import liste_objets, activer_objet, modifier_objet

urlpatterns = [
    path("", liste_objets, name="liste_objets"),
    path("activer/<int:objet_id>/", activer_objet, name="activer_objet"),
    path("modifier/<int:objet_id>/", modifier_objet, name="modifier_objet"),
    
]