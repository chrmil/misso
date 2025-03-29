from django.db import models
from django.urls import reverse
from django.utils.text import slugify

class Evenement(models.Model):
    titre = models.CharField(max_length=200,unique=True, blank=True)
    date = models.DateTimeField()
    description = models.TextField(blank=True, null=True)
    slug = models.SlugField(blank=True, editable=False)

    def __str__(self):
        return self.titre

    def save(self, *args, **kwargs):
        if not self.slug: 
            self.slug = slugify(f"{self.date.strftime('%Y-%m-%d')}-{self.titre}")
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse("evenement-detail", kwargs={'slug': self.slug})
