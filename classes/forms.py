# classes/forms.py
from django import forms
from .models import Classe
from utilisateurs.models import ProfilUtilisateur

class ClasseForm(forms.ModelForm):

    class Meta:
        model = Classe
        fields = ['nom', 'code']

