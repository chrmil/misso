from django.shortcuts import render, redirect, get_object_or_404
from .models import *


def page(request, page_nom):
    page = get_object_or_404(page, nom=page_nom)
    sections = Section.objects.filter(page=page)
    paragraphes = Paragraphe.objects.filter(section__in=sections)
    images = Image.objects.filter(image__in=sections)
    return render(request, 'menu/template.html', { 'page': page,'sections': sections, 'paragraphes': paragraphes, 'images': images })
