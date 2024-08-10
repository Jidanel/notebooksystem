# cours/forms.py
from django import forms
from .models import Matiere
from utilisateurs.models import ProfilUtilisateur, Departement

class MatiereForm(forms.ModelForm):
    class Meta:
        model = Matiere
        fields = ['nom', 'description', 'coefficient', 'departement', 'classe', 'enseignant']

    def __init__(self, *args, **kwargs):
        super(MatiereForm, self).__init__(*args, **kwargs)
        if 'departement' in self.data:
            try:
                departement_id = int(self.data.get('departement'))
                self.fields['enseignant'].queryset = ProfilUtilisateur.objects.filter(
                    enseignantdepartement__departement_id=departement_id
                ).order_by('nom')
            except (ValueError, TypeError):
                pass
        elif self.instance.pk:
            self.fields['enseignant'].queryset = ProfilUtilisateur.objects.filter(
                enseignantdepartement__departement=self.instance.departement
            ).order_by('nom')
        else:
            self.fields['enseignant'].queryset = ProfilUtilisateur.objects.none()
        self.fields['enseignant'].label_from_instance = lambda obj: f"{obj.nom}"
