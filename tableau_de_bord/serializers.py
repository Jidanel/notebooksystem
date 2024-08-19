from rest_framework import serializers
from eleves.models import Eleve
from classes.models import Classe
from notes.models import Note
from absences.models import Absence
from utilisateurs.models import ProfilUtilisateur

class EleveSerializer(serializers.ModelSerializer):
    class Meta:
        model = Eleve
        fields = ['id', 'nom', 'prenom', 'sexe', 'classe_actuelle']

class ClasseSerializer(serializers.ModelSerializer):
    eleves = EleveSerializer(many=True, read_only=True)

    class Meta:
        model = Classe
        fields = ['id', 'nom', 'code', 'eleves']

class NoteSerializer(serializers.ModelSerializer):
    classe_nom = serializers.CharField(source='classe.nom')
    eleve_sexe = serializers.CharField(source='eleve.sexe')
    matiere_nom = serializers.CharField(source='matiere.nom')

    class Meta:
        model = Note
        fields = ['classe_nom', 'sequence', 'eleve_sexe', 'note', 'matiere_nom']

class AbsenceSerializer(serializers.ModelSerializer):
    eleve_nom = serializers.CharField(source='eleve.nom', read_only=True)
    classe_nom = serializers.CharField(source='classe.nom', read_only=True)
    eleve_sexe = serializers.CharField(source='eleve.sexe', read_only=True)

    class Meta:
        model = Absence
        fields = ['id', 'eleve_nom', 'eleve_sexe', 'classe_nom', 'sequence', 'absences', 'justification', 'total']

class ProfilUtilisateurSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProfilUtilisateur
        fields = '__all__'
