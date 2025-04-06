from django.urls import path
from .views import *

urlpatterns = [
    path('<str:page_nom>/', page_view, name='page_view'),
]
