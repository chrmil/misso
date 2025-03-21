from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from django.urls import path
from .views import *

urlpatterns = [
    path('<str:restaurant_name>/', menu, name='menu'),
]

