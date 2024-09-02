from django import forms
from cours.models import Matiere
from classes.models import Classe
from .models import *

class ClasseMatiereSelectionForm(forms.Form):
    classe_matiere = forms.ChoiceField(choices=[], label="Sélectionner une classe et une matière")

    def __init__(self, *args, **kwargs):
        user = kwargs.pop('user', None)
        sequence = kwargs.pop('sequence', None)  # Vous pouvez passer la séquence dans les kwargs si nécessaire
        super().__init__(*args, **kwargs)
        if user:
            # Filtrer les matières en fonction de l'utilisateur connecté
            matieres = Matiere.objects.filter(enseignant=user.profilutilisateur)
            choices = []

            for matiere in matieres:
                # Vérifier s'il y a déjà des notes pour cette matière et séquence
                notes_existantes = Note.objects.filter(matiere=matiere, classe=matiere.classe, sequence=sequence).exists()

                # Si des notes existent déjà et l'utilisateur est un enseignant ou un AP, ne pas inclure cette matière
                if notes_existantes and user.profilutilisateur.role in ['Enseignant', 'AP']:
                    continue  # Passer à la prochaine matière

                choices.append((f"{matiere.classe.id}-{matiere.id}", f"{matiere.nom} - {matiere.classe.nom}"))

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
