from django.contrib import admin
from .models import Eleve

@admin.register(Eleve)
class EleveAdmin(admin.ModelAdmin):
    list_display = ('nom', 'prenom', 'classe_actuelle', 'matricule', 'statut')
    search_fields = ('nom', 'prenom', 'matricule')
