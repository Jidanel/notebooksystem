# absences/forms.py
from django import forms
from classes.models import Classe

class ClasseSequenceSelectionForm(forms.Form):
    classe = forms.ModelChoiceField(queryset=Classe.objects.all(), label="Sélectionner une classe")
    sequence = forms.ChoiceField(choices=[('Seq1', 'Séquence 1'), ('Seq2', 'Séquence 2'),('Seq3', 'Séquence 3'),('Seq4', 'Séquence 4'),('Seq5', 'Séquence 5'),], label="Sélectionner une séquence")

class ImpressionChoixForm(forms.Form):
    CHOIX_IMPRESSION = [
        ('sans_justifications', 'Imprimer sans justifications'),
        ('avec_justifications', 'Imprimer avec justifications')
    ]
    choix_impression = forms.ChoiceField(choices=CHOIX_IMPRESSION, widget=forms.RadioSelect, label="Choisissez le type d'impression")