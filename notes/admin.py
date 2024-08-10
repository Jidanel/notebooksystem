from django.contrib import admin
from .models import Note

@admin.register(Note)
class NoteAdmin(admin.ModelAdmin):
    list_display = ('eleve', 'enseignant', 'classe', 'matiere', 'sequence', 'note')
    list_filter = ('classe', 'matiere', 'sequence')
    search_fields = ('eleve__nom', 'eleve__prenom', 'matiere__nom')
