from django.contrib import admin
from .models import Classe

@admin.register(Classe)
class ClasseAdmin(admin.ModelAdmin):
    list_display = ('nom', 'code', 'enseignant_titulaire')
    search_fields = ('nom', 'code')
