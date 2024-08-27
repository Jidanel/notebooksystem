from django import forms
from cours.models import Matiere
from classes.models import Classe
from .models import *


class ClasseMatiereSelectionForm(forms.Form):
    classe_matiere = forms.ChoiceField(choices=[], label="Sélectionner une classe et une matière")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)
        if user:
            # Filtrer les matières en fonction de l'utilisateur connecté
            matieres = Matiere.objects.filter(enseignant=user.profilutilisateur)
            choices = [
                (f"{matiere.classe.id}-{matiere.id}", f"{matiere.nom} - {matiere.classe.nom}")
                for matiere in matieres
            ]
            self.fields['classe_matiere'].choices = choices

class NoteSaisieForm(forms.Form):
    eleve_id = forms.IntegerField(widget=forms.HiddenInput())
    eleve = forms.CharField(disabled=True, label="Élève")
    note = forms.FloatField(label="Note", min_value=0, max_value=20)

class SequenceSelectionForm(forms.Form):
    SEQUENCE_CHOICES = [
        ('Seq1', 'Séquence 1'),
        ('Seq2', 'Séquence 2'),
        ('Seq3', 'Séquence 3'),
        ('Seq4', 'Séquence 4'),
        ('Seq5', 'Séquence 5'),
    ]
    
    sequence = forms.ChoiceField(choices=SEQUENCE_CHOICES, label="Sélectionner une séquence")
