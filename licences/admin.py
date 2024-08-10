# licences/admin.py
from django.contrib import admin
from .models import Licence
from django.utils.crypto import get_random_string
from django.utils import timezone
from datetime import timedelta

@admin.action(description='Générer une nouvelle licence')
def generer_licence(modeladmin, request, queryset):
    # Générer un code unique pour la licence
    code = get_random_string(20)  # Longueur du code à 20 caractères
    duree_jours = 365  # Durée en jours pour la licence
    Licence.objects.create(code=code, duree_jours=duree_jours)  # Créez la licence avec une durée en jours
    modeladmin.message_user(request, f'Licence générée avec succès : {code}')

@admin.register(Licence)
class LicenceAdmin(admin.ModelAdmin):
    list_display = ('code', 'date_debut', 'date_expiration', 'active')
    actions = [generer_licence]
