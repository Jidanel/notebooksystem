from rest_framework import viewsets
from .serializers import EleveSerializer, ClasseSerializer, NoteSerializer, AbsenceSerializer, ProfilUtilisateurSerializer
from eleves.models import Eleve
from classes.models import Classe
from notes.models import Note
from absences.models import Absence
from utilisateurs.models import ProfilUtilisateur
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from utilisateurs.decorators import *
from django.db.models import Avg
from rest_framework.response import Response
from rest_framework.decorators import api_view
from cours.models import Matiere
from classes.models import Classe 
from notes.models import Note

class EleveViewSet(viewsets.ModelViewSet):
    queryset = Eleve.objects.all()
    serializer_class = EleveSerializer

class ClasseViewSet(viewsets.ModelViewSet):
    queryset = Classe.objects.all()
    serializer_class = ClasseSerializer

class NoteViewSet(viewsets.ModelViewSet):
    queryset = Note.objects.all()
    serializer_class = NoteSerializer

class AbsenceViewSet(viewsets.ModelViewSet):
    queryset = Absence.objects.all()
    serializer_class = AbsenceSerializer

class ProfilUtilisateurViewSet(viewsets.ModelViewSet):
    queryset = ProfilUtilisateur.objects.all()
    serializer_class = ProfilUtilisateurSerializer


@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def dashboard_view(request):
    return render(request, 'tableau_de_bord/dashboard.html')


@api_view(['GET'])
def get_sequences(request):
    sequences = Note.objects.values_list('sequence', flat=True).distinct()
    return Response(sequences)


@api_view(['GET'])
def meilleures_matieres_par_classe(request):
    resultats = []
    classes = Classe.objects.all()
    for classe in classes:
        matieres = Matiere.objects.filter(classe=classe)
        for matiere in matieres:
            moyenne_classe = Note.objects.filter(classe=classe, matiere=matiere).aggregate(Avg('note'))['note__avg']
            if moyenne_classe:
                resultats.append({
                    'classe': classe.nom,
                    'matiere': matiere.nom,
                    'moyenne': round(moyenne_classe, 2)
                })
    # Trier par moyenne décroissante
    resultats = sorted(resultats, key=lambda x: x['moyenne'], reverse=True)
    return Response(resultats)


@api_view(['GET'])
def meilleure_classe(request):
    resultats = []
    classes = Classe.objects.all()
    for classe in classes:
        moyenne_classe = Note.objects.filter(classe=classe).aggregate(Avg('note'))['note__avg']
        nombre_admis = Note.objects.filter(classe=classe, note__gte=10).count()
        if moyenne_classe:
            resultats.append({
                'classe': classe.nom,
                'moyenne': round(moyenne_classe, 2),
                'nombre_admis': nombre_admis
            })
    # Trier par moyenne décroissante
    resultats = sorted(resultats, key=lambda x: x['moyenne'], reverse=True)
    return Response(resultats)

@api_view(['GET'])
def meilleures_classes_par_sequence(request):
    sequence = request.query_params.get('sequence', None)
    if not sequence:
        return Response({"error": "Sequence is required"}, status=400)

    resultats = []
    classes = Classe.objects.all()

    for classe in classes:
        moyenne_classe = Note.objects.filter(classe=classe, sequence=sequence).aggregate(Avg('note'))['note__avg']
        nombre_admis = Note.objects.filter(classe=classe, sequence=sequence, note__gte=10).count()
        nombre_eleves = Note.objects.filter(classe=classe, sequence=sequence).count()

        if moyenne_classe and nombre_eleves > 0:
            taux_reussite = (nombre_admis / nombre_eleves) * 100
            resultats.append({
                'classe': classe.nom,
                'moyenne': round(moyenne_classe, 2),
                'nombre_admis': nombre_admis,
                'taux_reussite': round(taux_reussite, 2)
            })

    # Trier par taux de réussite décroissant et prendre les 3 meilleures classes
    resultats = sorted(resultats, key=lambda x: x['taux_reussite'], reverse=True)[:3]
    return Response(resultats)


from django.db.models import Avg

@api_view(['GET'])
def matieres_avec_moins_de_reussite_par_trimestre(request):
    resultats = []
    classes = Classe.objects.all()
    for classe in classes:
        sequences = Note.objects.filter(classe=classe).values_list('sequence', flat=True).distinct()
        for sequence in sequences:
            matieres = Matiere.objects.filter(classe=classe)
            pire_matiere = None
            pire_moyenne = None

            for matiere in matieres:
                moyenne_classe = Note.objects.filter(classe=classe, matiere=matiere, sequence=sequence).aggregate(Avg('note'))['note__avg']
                
                if moyenne_classe is not None:
                    if pire_moyenne is None or moyenne_classe < pire_moyenne:
                        pire_moyenne = moyenne_classe
                        pire_matiere = matiere

            if pire_moyenne is not None:
                resultats.append({
                    'classe': classe.nom,
                    'matiere': pire_matiere.nom,
                    'sequence': sequence,
                    'moyenne': round(pire_moyenne, 2)
                })
    
    # Trier par moyenne croissante pour avoir la matière avec la moins bonne moyenne en tête
    resultats = sorted(resultats, key=lambda x: x['moyenne'])



