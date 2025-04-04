from django.db import models
from django.conf import settings

class Page(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    emplacement = models.URLField(max_length=500, blank=True, null=True)
    titre = models.TextField(max_length=500, blank=True, null=True)
    sous_titre = models.TextField(max_length=500, blank=True, null=True)
    image_path = models.CharField(max_length=255, blank=True, null=True) 
    
    def __str__(self):
        return self.nom

class Section(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    page = models.ForeignKey(Page, on_delete=models.CASCADE)
    titre = models.TextField(max_length=500, blank=True, null=True)
    sous_titre = models.TextField(max_length=500, blank=True, null=True)
    visible = models.BooleanField(default=True) 
    def __str__(self):
        return self.page.nom+"/"+self.nom

class Paragraphe(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    titre = models.TextField(max_length=500, blank=True, null=True)
    sous_titre = models.TextField(max_length=500, blank=True, null=True)
    texte = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.section.page.nom+"/"+self.section.nom+"/"+self.nom

class Image(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    section = models.ForeignKey(Section, on_delete=models.CASCADE)
    image_path = models.CharField(max_length=300, blank=True, null=True) 
    def __str__(self):
        return self.section.page.nom+"/"+self.section.nom+"/"+self.nom
