from django import forms
from .models import Eleve
from classes.models import *

class EleveForm(forms.ModelForm):
    class Meta:
        model = Eleve
        fields = ['nom', 'prenom', 'sexe', 'date_naissance', 'lieu_naissance', 'adresse', 'classe_actuelle', 'matricule', 'statut', 'contact_parent']

    def __init__(self, *args, **kwargs):
        super(EleveForm, self).__init__(*args, **kwargs)
        self.fields['prenom'].required = False
        self.fields['contact_parent'].required = False


class ClasseSelectionForm(forms.Form):
    classe = forms.ModelChoiceField(queryset=Classe.objects.all(), label="Sélectionner une classe")
    file = forms.FileField(label="Choisir un fichier Excel")