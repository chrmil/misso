from django.db import models

class Restaurant(models.Model):
    name = models.CharField(max_length=100, unique=True)
    location = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return self.name

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    
    def __str__(self):
        return self.name

class MenuItem(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    image_path = models.CharField(max_length=255, blank=True, null=True)  # Store static file path
    
    def __str__(self):
        return self.name