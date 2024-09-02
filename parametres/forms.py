from django import forms
from .models import ParametresEtablissement

class ParametresEtablissementForm(forms.ModelForm):
    class Meta:
        model = ParametresEtablissement
        fields = [
            'nom_etablissement_fr', 'nom_etablissement_en', 'bp_fr', 'bp_en',
            'telephone_fr', 'telephone_en', 'ville_fr', 'ville_en',
            'annee_scolaire', 'logo', 'type_enseignement'
        ]
        widgets = {
            'nom_etablissement_fr': forms.TextInput(attrs={'class': 'form-control'}),
            'nom_etablissement_en': forms.TextInput(attrs={'class': 'form-control'}),
            'bp_fr': forms.TextInput(attrs={'class': 'form-control'}),
            'bp_en': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone_fr': forms.TextInput(attrs={'class': 'form-control'}),
            'telephone_en': forms.TextInput(attrs={'class': 'form-control'}),
            'ville_fr': forms.TextInput(attrs={'class': 'form-control'}),
            'ville_en': forms.TextInput(attrs={'class': 'form-control'}),
            'annee_scolaire': forms.TextInput(attrs={'class': 'form-control'}),
            'logo': forms.URLInput(attrs={'class': 'form-control'}),
            'type_enseignement': forms.Select(attrs={'class': 'form-control'}),
        }
