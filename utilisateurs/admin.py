from django.contrib import admin
from .models import *

class ProfilUtilisateurAdmin(admin.ModelAdmin):
    list_display = ('nom','utilisateur', 'matricule','sexe', 'role', 'code_de_securite','actif')

admin.site.register(ProfilUtilisateur, ProfilUtilisateurAdmin)
