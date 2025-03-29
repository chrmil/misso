from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import Utilisateur
from datetime import date, timedelta

class InscriptionForm(UserCreationForm):
    date_de_naissance = forms.DateField(widget=forms.DateInput(attrs={'type': 'date'}))
    genre = forms.ChoiceField(choices=Utilisateur.GENRE_CHOIX, widget=forms.Select())
    
    password2 = forms.CharField(
        label="Confirmation du mot de passe",
        widget=forms.PasswordInput,
        help_text=""  # On supprime le message par défaut
    )

    password1 = forms.CharField(
        label="Mot de passe",
        widget=forms.PasswordInput,
        help_text=""  # Enlève tous les messages d'aide par défaut
    )

    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'date_de_naissance', 'genre', 'password1', 'password2']

    def clean_date_de_naissance(self):
        date_naissance = self.cleaned_data.get("date_de_naissance")

        if date_naissance > date.today():
            raise forms.ValidationError("La date de naissance ne peut pas être dans le futur.")

        age_minimum = date.today() - timedelta(days=13*365)
        if date_naissance > age_minimum:
            raise forms.ValidationError("Vous devez avoir au moins 13 ans pour vous inscrire.")

        return date_naissance

    def clean_email(self):
        email = self.cleaned_data.get("email")
        if Utilisateur.objects.filter(email=email).exists():
            raise forms.ValidationError("Cet email est déjà utilisé. Veuillez en choisir un autre.")
        return email
    

class ProfilForm(forms.ModelForm):
    class Meta:
        model = Utilisateur
        fields = ['username', 'email', 'date_de_naissance', 'genre']
        widgets = {
            'date_de_naissance': forms.DateInput(attrs={'type': 'date'}),
        }

    def clean_email(self):
        """Validation pour s'assurer que l'email est unique."""
        email = self.cleaned_data.get('email')
        if Utilisateur.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError("Cet email est déjà utilisé par un autre utilisateur.")
        return email

    def clean_date_de_naissance(self):
        """Validation pour s'assurer que la date de naissance est valide."""
        date_de_naissance = self.cleaned_data.get('date_de_naissance')
        if date_de_naissance:
            from datetime import date
            if date_de_naissance > date.today():
                raise forms.ValidationError("La date de naissance ne peut pas être dans le futur.")
        else:
            raise forms.ValidationError("La date de naissance est obligatoire.")
        return date_de_naissance
