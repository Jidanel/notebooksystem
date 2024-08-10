from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import *
from django.forms import ModelForm
from django import forms
from django.contrib.auth.forms import SetPasswordForm

class CreateUserForm(UserCreationForm):
    class Meta:
        model = User
        fields = ['username', 'password1', 'password2']

class ProfileForm(ModelForm):
    class Meta:
        model = ProfilUtilisateur
        fields = ['nom', 'matricule', 'code_de_securite', 'profile_img', 'sexe']
        exclude = ['utilisateur', 'role']  # Exclure le champ "role" du formulaire

class RoleAssignmentForm(ModelForm):
    class Meta:
        model = ProfilUtilisateur
        fields = ['role']

class ResetPasswordForm(SetPasswordForm):
    new_password = forms.CharField(widget=forms.PasswordInput, label="Nouveau mot de passe")

    def __init__(self, user, *args, **kwargs):
        super().__init__(user, *args, **kwargs)

class SecurityCodeForm(forms.ModelForm):
    code_de_securite = forms.CharField(widget=forms.PasswordInput, label="Code de sécurité")

    class Meta:
        model = ProfilUtilisateur
        fields = ['code_de_securite']

class NotificationForm(forms.Form):
    message = forms.CharField(widget=forms.Textarea, label='Message')

class DepartementForm(forms.ModelForm):
    class Meta:
        model = Departement
        fields = ['nom', 'description', 'chef_departement']

    def __init__(self, *args, **kwargs):
        super(DepartementForm, self).__init__(*args, **kwargs)
        self.fields['chef_departement'].queryset = ProfilUtilisateur.objects.filter(role='AP')
        self.fields['chef_departement'].label_from_instance = lambda obj: f"{obj.nom}"


class AssignerEnseignantForm(forms.ModelForm):
    departements = forms.ModelMultipleChoiceField(
        queryset=Departement.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=True,
        label="Départements"
    )

    class Meta:
        model = ProfilUtilisateur
        fields = ['departements']

class AssignationForm(forms.ModelForm):
    enseignant = forms.ModelChoiceField(queryset=ProfilUtilisateur.objects.all(), label="Enseignant")
    departements = forms.ModelMultipleChoiceField(queryset=Departement.objects.all(), label="Départements", widget=forms.CheckboxSelectMultiple)
    is_chef_departement = forms.BooleanField(label="Est chef de département", required=False)

    class Meta:
        model = EnseignantDepartement
        fields = ['enseignant', 'departements', 'is_chef_departement']
