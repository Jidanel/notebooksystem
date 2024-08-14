from django.contrib import admin
from django.urls import path, include
from .views import *



urlpatterns = [
    path('parametres/', gerer_parametres_etablissement, name='gestion_parametres'),
]

