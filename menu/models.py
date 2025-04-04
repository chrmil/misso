from django.db import models

class Restaurant(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    emplacement = models.CharField(max_length=255, blank=True, null=True)
    titre = models.TextField(max_length=500, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image_path = models.CharField(max_length=255, blank=True, null=True) 
    
    def __str__(self):
        return self.nom
    
class Menu(models.Model):
    nom = models.CharField(max_length=100, unique=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    visible = models.BooleanField(default=True)
    def __str__(self):
        return self.nom

class CategorieBoisson(models.Model):
    nom  = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.nom

class CategoriePlat(models.Model):
    nom  = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)
    def __str__(self):
        return self.nom

    
class Plat(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    categorie = models.ForeignKey(CategoriePlat, on_delete=models.CASCADE)
    nom  = models.CharField(max_length=100, unique=True)
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image_path = models.CharField(max_length=255, blank=True, null=True) 
    def __str__(self):
        return self.nom
    
class AccompagnementPlat(models.Model):
    plat = models.ForeignKey(Plat, on_delete=models.CASCADE)
    nom  = models.CharField(max_length=100, unique=True)
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image_path = models.CharField(max_length=255, blank=True, null=True) 
    def __str__(self):
        return self.nom
 

class Boisson(models.Model):
    menu = models.ForeignKey(Menu, on_delete=models.CASCADE)
    categorie = models.ForeignKey(CategorieBoisson, on_delete=models.CASCADE)
    nom  = models.CharField(max_length=100, unique=True)
    prixVerre  =  models.DecimalField(max_digits=6, decimal_places=2, blank=False, null=True)
    prixBouteille = models.DecimalField(max_digits=6, decimal_places=2, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    image_path = models.CharField(max_length=255, blank=True, null=True) 
    def __str__(self):
        return self.nom
    
    
class AccompagnementBoisson(models.Model):
    boisson = models.ForeignKey(Boisson, on_delete=models.CASCADE)
    nom  = models.CharField(max_length=100, unique=True)
    prix = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image_path = models.CharField(max_length=255, blank=True, null=True) 
    def __str__(self):
        return self.nom
  