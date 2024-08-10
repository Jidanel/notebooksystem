from django.contrib import admin
from .models import Matiere

@admin.register(Matiere)
class MatiereAdmin(admin.ModelAdmin):
    list_display = ('nom', 'coefficient', 'departement', 'classe', 'enseignant')
    search_fields = ('nom',)
