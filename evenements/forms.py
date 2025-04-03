from urllib import request
from django import forms
from evenements.models import *
from datetime import date, datetime, timedelta
from datetime import time
class EvenementForm(forms.ModelForm):
    titre = forms.CharField(
        label="Titre",
        help_text=""
        )
    date = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    debut = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    fin = forms.TimeField(widget=forms.TimeInput(attrs={'type': 'time'}))
    description = forms.CharField(
        label="Description",
        help_text=""
    )    
    class Meta(Evenement):
        model = Evenement
        fields = ['titre', 'date', 'debut','fin','description']
    def clean_date(self):
        date = self.cleaned_data.get("date")
        if date < date.today(): #pas de date passée
            raise forms.ValidationError("La date ne peut pas être dans le passé.")
        if date <= date.today()+timedelta(days=5): #au moins 3 jours entre date et aujourd'hui
              raise forms.ValidationError("La date doit être dans au moins 5 jours.")
        return date
    def clean_fin(self):
        fin= self.cleaned_data.get("fin")
        debut = self.cleaned_data.get("debut")
        if not(fin):
             raise forms.ValidationError("L'horaire de fin doit être renseigné.")
        if debut and debut==fin:
             raise forms.ValidationError("L'horaire de fin et l'horaire de début ne peuvent pas être égaux.")
        if debut and fin!=time(0,0) and debut >  fin: 
            raise forms.ValidationError("L'horaire de début ne peut pas être après l'horaire de fin.")
        return fin

    def clean_debut(self):
        debut = self.cleaned_data.get("debut")
        fin=self.cleaned_data.get("fin")
        if not(debut):
             raise forms.ValidationError("L'horaire de début doit être renseigné.")
        if fin and debut==fin:
             raise forms.ValidationError("L'horaire de fin et l'horaire de début ne peuvent pas être égaux.")
        if fin and fin!=time(0,0) and debut >  fin:
            raise forms.ValidationError("L'horaire de début ne peut pas être après l'horaire de fin.")
        return debut
        