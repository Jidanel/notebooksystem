from django import forms
from .models import Matiere
from utilisateurs.models import ProfilUtilisateur
from parametres.models import ParametresEtablissement

class MatiereForm(forms.ModelForm):
    groupe = forms.ChoiceField(choices=[], required=True, label="Groupe")

    class Meta:
        model = Matiere
        fields = ['nom', 'coefficient', 'departement', 'classe', 'enseignant', 'groupe']
        widgets = {
            'nom': forms.TextInput(attrs={'class': 'form-control'}),
            'coefficient': forms.NumberInput(attrs={'class': 'form-control'}),
            'departement': forms.Select(attrs={'class': 'form-control'}),
            'classe': forms.Select(attrs={'class': 'form-control'}),
            'enseignant': forms.Select(attrs={'class': 'form-control'}),
            'groupe': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        super(MatiereForm, self).__init__(*args, **kwargs)

        # Logique pour filtrer les enseignants par département
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

        # Définition des choix de groupes en fonction du type d'enseignement
        parametres = ParametresEtablissement.objects.first()
        if parametres:
            if parametres.type_enseignement == 'bilingue':
                self.fields['groupe'].choices = [
                    ('groupe_1', 'Groupe 1'),
                    ('groupe_2', 'Groupe 2'),
                    ('groupe_3', 'Groupe 3'),
                    
                ]
            elif parametres.type_enseignement == 'technique':
                self.fields['groupe'].choices = [
                    ('enseignement_general', 'Enseignement Général'),
                    ('enseignement_professionnel', 'Enseignement Professionnel'),
                    ('enseignement_divers', 'Enseignement Divers'),
                ]
            elif parametres.type_enseignement == 'general':
                self.fields['groupe'].choices = [
                    ('groupe_1', 'Groupe 1'),
                    ('groupe_2', 'Groupe 2'),
                    ('groupe_3', 'Groupe 3'),
                ]

        # Remplissage du champ groupe avec la valeur existante si elle est définie
        if self.instance.pk and self.instance.groupe:
            self.fields['groupe'].initial = self.instance.groupe
