from django import forms
from evenements.models import *
from datetime import date, timedelta

class EvenementForm():
    titre = forms.CharField(
        label="Titre",
        help_text=""
        )
    date = forms.DateTimeField(widget=forms.DateTimeInput(attrs={'type': 'date'}))

    description = forms.CharField(
        label="Description",
        help_text=""
    )    
    class Meta(Evenement):
        model = Evenement
        fields = ['date', 'titre', 'description']

    def clean_date(self):
        date = self.cleaned_data.get("date")

        if date < date.today():
            raise forms.ValidationError("La date ne peut pas être dans le passé.")
        return date


