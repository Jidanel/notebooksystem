from django import forms
from .models import ParametresEtablissement

class ParametresEtablissementForm(forms.ModelForm):
    class Meta:
        model = ParametresEtablissement
        fields = ['nom_etablissement_fr', 'nom_etablissement_en', 'bp_fr', 'bp_en', 
                  'telephone_fr', 'telephone_en', 'ville_fr', 'ville_en', 
                  'annee_scolaire', 'logo']
