from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.urls import path
from .views import *
from evenements.views import *
from django.views.generic.dates import *
from evenements.models import Evenement



urlpatterns = [
    path(
      "",
      EvenementArchiveIndexView.as_view(model=Evenement, date_field="date"),
      name="evenements",
  ),
    path("<slug:slug>/", EvenementDetailView.as_view(), name="evenement-detail"),
]

