# classes/forms.py
from django import forms
from .models import Classe
from utilisateurs.models import ProfilUtilisateur

class ClasseForm(forms.ModelForm):
    enseignant_titulaire = forms.ModelChoiceField(
        queryset=ProfilUtilisateur.objects.all(),
        required=False,
        label='Enseignant titulaire',
        widget=forms.Select()
    )

    class Meta:
        model = Classe
        fields = ['nom', 'code', 'enseignant_titulaire']

    def __init__(self, *args, **kwargs):
        super(ClasseForm, self).__init__(*args, **kwargs)
        self.fields['enseignant_titulaire'].label_from_instance = lambda obj: f"{obj.nom}"
