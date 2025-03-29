from django.shortcuts import render
from django.utils import timezone
from django.views.generic.detail import DetailView
from evenements.models import Evenement
from django.views.generic.dates import *



    
class EvenementArchiveIndexView(ArchiveIndexView):
    model = Evenement
    queryset = Evenement.objects.all()
    date_field = "date"
    allow_future = True


class EvenementDetailView(DetailView):
    model = Evenement
    template = "evenement_detail.html"
    context_objet_name="evenement"
    slug_field = "slug"
    slug_url_kwarg = "slug"
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        year = self.kwargs.get('year')
        month = self.kwargs.get('month')
        slug = self.kwargs.get('slug')
        return context
    


   

