from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur
from datetime import date, timedelta

class InscriptionForm(UserCreationForm):
    date_de_naissance = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    genre = forms.ChoiceField(choices=Utilisateur.GENRE_CHOIX, widget=forms.Select())

    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'date_de_naissance', 'genre', 'password1', 'password2']

    def clean_date_de_naissance(self):
        date_naissance = self.cleaned_data.get("date_de_naissance")

        # Vérifier si la date est dans le futur
        if date_naissance > date.today():
            raise forms.ValidationError("La date de naissance ne peut pas être dans le futur.")

        # Vérifier si l'utilisateur a au moins 13 ans
        age_minimum = date.today() - timedelta(days=13*365)
        if date_naissance > age_minimum:
            raise forms.ValidationError("Vous devez avoir au moins 13 ans pour vous inscrire.")

        return date_naissance

def clean_email(self):
    email = self.cleaned_data.get("email")
    if Utilisateur.objects.filter(email=email).exists():
        raise forms.ValidationError("Cet email est déjà utilisé. Veuillez en choisir un autre.")
    return email
