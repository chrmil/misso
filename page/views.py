from django.shortcuts import render, redirect, get_object_or_404
from .models import *


def page_view(request, page_nom):
    page = get_object_or_404(Page, nom=page_nom)
    sections = Section.objects.filter(page=page).order_by("priorite")
    paragraphes = Paragraphe.objects.filter(section__in=sections).order_by("priorite")
    images = Image.objects.filter(paragraphe__in=paragraphes).order_by("priorite")
    return render(request, 'page/template.html', { 'page': page,'sections': sections, 'paragraphes': paragraphes, 'images': images })
