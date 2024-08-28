from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import ClasseMatiereSelectionForm
from .models import Note
from eleves.models import Eleve
from classes.models import Classe
from cours.models import *
from utilisateurs.models import *
from django.db.models import Q
from utilisateurs.decorators import *
from django.db.models import Max, Min, Avg, Count
import math
from django.core.paginator import Paginator
from classes.models import *
from parametres.models import *
from django.http import HttpResponse
from django.template.loader import render_to_string
from xhtml2pdf import pisa
from absences.models import *
from django.db.models import Sum
from django.template.loader import get_template
from .forms import *

@login_required
def selection_classe_matiere(request, sequence):
    if request.method == 'POST':
        form = ClasseMatiereSelectionForm(request.POST, user=request.user)
        if form.is_valid():
            classe_matiere = form.cleaned_data['classe_matiere']
            classe_id, matiere_id = map(int, classe_matiere.split('-'))
            return redirect('saisie_notes', sequence=sequence, classe_id=classe_id, matiere_id=matiere_id)
    else:
        form = ClasseMatiereSelectionForm(user=request.user)
    
    return render(request, 'notes/selection_classe_matiere.html', {'form': form, 'sequence': sequence})

@login_required
def saisie_notes(request, sequence, classe_id, matiere_id):
    classe = get_object_or_404(Classe, id=classe_id)
    matiere = get_object_or_404(Matiere, id=matiere_id)
    eleves = Eleve.objects.filter(classe_actuelle=classe).order_by('nom')
    notes_existantes = {note.eleve.id: note.note for note in Note.objects.filter(classe=classe, matiere=matiere, sequence=sequence)}

    if request.method == 'POST':
        all_filled = True
        for eleve in eleves:
            note_value = request.POST.get(f'note_{eleve.id}')
            if not note_value or note_value == "" or float(note_value) == 0:
                all_filled = False
                break

        if all_filled and len(eleves) == len(notes_existantes):
            completed_status = True
        else:
            completed_status = False

        if all_filled:
            for eleve in eleves:
                note_value = request.POST.get(f'note_{eleve.id}')
                Note.objects.update_or_create(
                    eleve=eleve,
                    matiere=matiere,
                    sequence=sequence,
                    defaults={'note': note_value, 'classe': classe, 'enseignant': request.user.profilutilisateur, 'completed': completed_status}
                )
            messages.success(request, "Les notes ont été enregistrées avec succès.")

            # Calculer les statistiques après la saisie des notes
            stats = calcul_statistiques_matiere(classe, matiere, sequence)
            return render(request, 'notes/statistiques_matiere.html', {
                'classe': classe,
                'matiere': matiere,
                'sequence': sequence,
                'stats': stats,
            })
        else:
            messages.error(request, "Veuillez remplir toutes les notes avant d'enregistrer.")

    return render(request, 'notes/saisie_notes.html', {
        'eleves': eleves,
        'classe': classe,
        'matiere': matiere,
        'sequence': sequence,
        'notes_existantes': notes_existantes
    })


@login_required
def menu_gestion_trimestres(request):
    return render(request, 'notes/menu_gestion_trimestres.html')

@login_required
def menu_gestion_trimestre_1(request):
    return render(request, 'notes/menu_gestion_trimestre_1.html')

@role_required(allowed_roles=['AP','Admin_'])
@login_required
def gestion_stats_departements(request):
    return render(request, 'notes/menu_statistiques_departement.html')


@login_required
def bulletins_et_stats(request):
    query = request.GET.get('q')
    classes = Classe.objects.all().order_by('nom')

    if query:
        classes = classes.filter(nom__icontains=query)

    paginator = Paginator(classes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'notes/bulletins_et_stats.html',  {'page_obj': page_obj, 'query': query})

@login_required
def liste_notes_completes(request):
    enseignant = request.user.profilutilisateur
    notes_completes = Note.objects.filter(
        Q(enseignant=enseignant) | Q(matiere__enseignant=enseignant),
        completed=True
    ).distinct('classe', 'matiere', 'sequence')
    return render(request, 'notes/liste_notes_completes.html', {'notes_completes': notes_completes})

# Alias pour la séquence 2
@login_required
def selection_classe_matiere_seq2(request):
    return selection_classe_matiere(request, 'Seq2')

@login_required
def saisie_notes_seq2(request, classe_id, matiere_id):
    return saisie_notes(request, 'Seq2', classe_id, matiere_id)

def calcul_statistiques_matiere(classe, matiere, sequence):
    notes = Note.objects.filter(classe=classe, matiere=matiere, sequence=sequence)
    
    total_eleves = notes.count()
    nb_garcons = notes.filter(eleve__sexe='Masculin').count()
    nb_filles = notes.filter(eleve__sexe='Feminin').count()

    nb_garcons_moyenne = notes.filter(eleve__sexe='Masculin', note__gte=10).count()
    nb_filles_moyenne = notes.filter(eleve__sexe='Feminin', note__gte=10).count()
    nb_eleves_moyenne = notes.filter(note__gte=10).count()

    stats = {
        'max_note': round(notes.aggregate(Max('note'))['note__max'], 2),
        'min_note': round(notes.aggregate(Min('note'))['note__min'], 2),
        'moyenne_classe': round(notes.aggregate(Avg('note'))['note__avg'], 2),
        'nb_garcons_moyenne': nb_garcons_moyenne,
        'nb_filles_moyenne': nb_filles_moyenne,
        'nb_eleves_moyenne': nb_eleves_moyenne,
        'nb_garcons_sous_moyenne': notes.filter(eleve__sexe='Masculin', note__lt=10).count(),
        'nb_filles_sous_moyenne': notes.filter(eleve__sexe='Feminin', note__lt=10).count(),
        'nb_eleves_sous_moyenne': notes.filter(note__lt=10).count(),
        'pourcentage_reussite_garcons': round((nb_garcons_moyenne / nb_garcons) * 100, 2) if nb_garcons > 0 else 0,
        'pourcentage_reussite_filles': round((nb_filles_moyenne / nb_filles) * 100, 2) if nb_filles > 0 else 0,
        'pourcentage_reussite_total': round((nb_eleves_moyenne / total_eleves) * 100, 2) if total_eleves > 0 else 0,
        'pourcentage_echec_garcons': round((1 - (nb_garcons_moyenne / nb_garcons)) * 100, 2) if nb_garcons > 0 else 0,
        'pourcentage_echec_filles': round((1 - (nb_filles_moyenne / nb_filles)) * 100, 2) if nb_filles > 0 else 0,
        'pourcentage_echec_total': round((1 - (nb_eleves_moyenne / total_eleves)) * 100, 2) if total_eleves > 0 else 0,
    }

    # Calcul de l'écart-type
    moyenne_classe = stats['moyenne_classe']
    variance = sum((note.note - moyenne_classe) ** 2 for note in notes) / total_eleves if total_eleves > 0 else 0
    stats['ecart_type'] = round(math.sqrt(variance), 2)

    # Classer les notes des élèves en ordre décroissant et calculer les rangs
    notes = notes.order_by('-note')
    for idx, note in enumerate(notes, start=1):
        note.rang = idx  # Calcul dynamique du rang
        if note.note < 10:
            note.appreciation = "NON ACQUIS"
        elif 10 <= note.note < 13:
            note.appreciation = "EN COURS"
        else:
            note.appreciation = "ACQUIS"
        note.save(update_fields=['rang', 'appreciation'])

    # Ajouter le classement des élèves aux statistiques
    stats['classement'] = notes

    return stats

def calculer_moyenne_sequence_eleve(eleve, sequence):
    notes = Note.objects.filter(eleve=eleve, sequence=sequence)
    total_notes = sum(note.note * note.matiere.coefficient for note in notes)
    total_coefficients = sum(note.matiere.coefficient for note in notes)

    if total_coefficients > 0:
         return round(total_notes / total_coefficients, 2)
    return 0  # Retourne 0 si l'élève n'a aucune note

def calcul_statistiques_classe(sequence, classe):
    eleves = Eleve.objects.filter(classe_actuelle=classe)
    moyennes = []
    
    for eleve in eleves:
        moyenne_sequence = calculer_moyenne_sequence_eleve(eleve, sequence)
        moyennes.append({
            'eleve': eleve,
            'moyenne_sequence': moyenne_sequence
        })

    moyennes.sort(key=lambda x: x['moyenne_sequence'], reverse=True)
    
    moyenne_max = round(max(moyennes, key=lambda x: x['moyenne_sequence'])['moyenne_sequence'], 2) if moyennes else 0
    moyenne_min = round(min(moyennes, key=lambda x: x['moyenne_sequence'])['moyenne_sequence'], 2) if moyennes else 0
    moyenne_generale = round(sum(x['moyenne_sequence'] for x in moyennes) / len(moyennes), 2) if moyennes else 0

    # Calcul de l'écart-type
    variance = sum((x['moyenne_sequence'] - moyenne_generale) ** 2 for x in moyennes) / len(moyennes) if moyennes else 0
    ecart_type = round(math.sqrt(variance), 2) if moyennes else 0

    # Taux de réussite
    nb_reussites = sum(1 for x in moyennes if x['moyenne_sequence'] >= 10)
    taux_reussite = round((nb_reussites / len(moyennes)) * 100, 2) if moyennes else 0

    stats_classe = {
        'moyenne_max': moyenne_max,
        'moyenne_min': moyenne_min,
        'moyenne_generale': moyenne_generale,
        'ecart_type': ecart_type,
        'taux_reussite': taux_reussite,
        'classement': moyennes,
    }

    return stats_classe


@login_required
def afficher_bulletins(request, sequence, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)
    stats_classe = calcul_statistiques_classe(sequence, classe)
    
    return render(request, 'bulletins/afficher_bulletins.html', {
        'classe': classe,
        'sequence': sequence,
        'stats_classe': stats_classe,
    })

@login_required
def afficher_statistiques_matiere(request, sequence, classe_id, matiere_id):
    # Récupérer les objets Classe et Matière
    classe = get_object_or_404(Classe, id=classe_id)
    matiere = get_object_or_404(Matiere, id=matiere_id)

    # S'assurer que `sequence` est bien traité comme une chaîne de caractères
    sequence = str(sequence)

    # Récupérer les notes pour la classe, la matière et la séquence
    notes = Note.objects.filter(classe=classe, matiere=matiere, sequence=sequence)

    # Calculer les statistiques
    stats = calcul_statistiques_matiere(classe, matiere, sequence)

    # Passer les informations au template
    context = {
        'classe': classe,
        'matiere': matiere,
        'sequence': sequence,
        'stats': stats,
    }

    return render(request, 'notes/statistiques_matiere.html', context)
# Nouvelle fonction pour calculer la moyenne trimestrielle d'un élève pour une matière
def calculer_moyenne_trimestrielle(eleve, matiere):
    seq1_note = Note.objects.filter(eleve=eleve, matiere=matiere, sequence='Seq1').first()
    seq2_note = Note.objects.filter(eleve=eleve, matiere=matiere, sequence='Seq2').first()

    if seq1_note and seq2_note:
        moyenne_trimestrielle = round((seq1_note.note + seq2_note.note) / 2, 2)
    elif seq1_note:
        moyenne_trimestrielle = seq1_note.note
    elif seq2_note:
        moyenne_trimestrielle = seq2_note.note
    else:
        moyenne_trimestrielle = 0

    return moyenne_trimestrielle

# Calcul des statistiques trimestrielles pour une classe
def calcul_statistiques_trimestre(classe):
    eleves = Eleve.objects.filter(classe_actuelle=classe)
    moyennes_trimestrielles = []

    for eleve in eleves:
        total_notes = 0
        total_coefficients = 0

        matieres = Matiere.objects.filter(classe=classe)
        for matiere in matieres:
            moyenne_trimestrielle = calculer_moyenne_trimestrielle(eleve, matiere)
            total_notes += moyenne_trimestrielle * matiere.coefficient
            total_coefficients += matiere.coefficient

        moyenne_generale_trimestrielle = round(total_notes / total_coefficients, 2) if total_coefficients > 0 else 0
        moyennes_trimestrielles.append({
            'eleve': eleve,
            'moyenne_trimestrielle': moyenne_generale_trimestrielle
        })

    # Statistiques sur les moyennes trimestrielles
    moyennes_trimestrielles.sort(key=lambda x: x['moyenne_trimestrielle'], reverse=True)
    moyenne_max = round(max(moyennes_trimestrielles, key=lambda x: x['moyenne_trimestrielle'])['moyenne_trimestrielle'], 2)
    moyenne_min = round(min(moyennes_trimestrielles, key=lambda x: x['moyenne_trimestrielle'])['moyenne_trimestrielle'], 2)
    moyenne_generale = round(sum(x['moyenne_trimestrielle'] for x in moyennes_trimestrielles) / len(moyennes_trimestrielles), 2)

    # Calcul de l'écart-type
    variance = sum((x['moyenne_trimestrielle'] - moyenne_generale) ** 2 for x in moyennes_trimestrielles) / len(moyennes_trimestrielles)
    ecart_type = round(math.sqrt(variance), 2)

    # Taux de réussite
    nb_reussites = sum(1 for x in moyennes_trimestrielles if x['moyenne_trimestrielle'] >= 10)
    taux_reussite = round((nb_reussites / len(moyennes_trimestrielles)) * 100, 2)

    stats_classe_trimestre = {
        'moyenne_max': moyenne_max,
        'moyenne_min': moyenne_min,
        'moyenne_generale': moyenne_generale,
        'ecart_type': ecart_type,
        'taux_reussite': taux_reussite,
        'classement': moyennes_trimestrielles,
    }

    return stats_classe_trimestre

@login_required
def afficher_statistiques_trimestre(request, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)
    stats_classe_trimestre = calcul_statistiques_trimestre(classe)
    
    return render(request, 'notes/statistiques_trimestre.html', {
        'classe': classe,
        'stats_classe_trimestre': stats_classe_trimestre,
    })

@login_required
def afficher_statistiques_sequence(request, classe_id, sequence):
    classe = get_object_or_404(Classe, id=classe_id)

    # Calculer les statistiques pour la séquence donnée
    stats_classe = calcul_statistiques_classe(sequence, classe)
    
    return render(request, 'notes/statistiques_sequence.html', {
        'classe': classe,
        'sequence': sequence,
        'stats_classe': stats_classe,
    })
@login_required
def afficher_statistiques_trimestre(request, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)
    stats_classe_trimestre = calcul_statistiques_trimestre(classe)
    
    return render(request, 'notes/statistiques_trimestre.html', {
        'classe': classe,
        'stats_classe_trimestre': stats_classe_trimestre,
    })

@login_required
def afficher_bulletins_trimestriels(request, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)
    eleves = Eleve.objects.filter(classe_actuelle=classe).order_by('nom')
    parametres = ParametresEtablissement.objects.first()

    type_enseignement = parametres.type_enseignement if parametres else None

    groupes_definition = []
    if type_enseignement == 'technique':
        groupes_definition = [
            {'nom': 'Enseignement Général', 'matieres': Matiere.objects.filter(classe=classe, groupe='enseignement_general').order_by('nom')},
            {'nom': 'Enseignement Professionnel', 'matieres': Matiere.objects.filter(classe=classe, groupe='enseignement_professionnel').order_by('nom')},
            {'nom': 'Enseignement Divers', 'matieres': Matiere.objects.filter(classe=classe, groupe='enseignement_divers').order_by('nom')},
        ]
    elif type_enseignement == 'bilingue':
        groupes_definition = [
            {'nom': 'Groupe 1', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_1').order_by('nom')},
            {'nom': 'Groupe 2', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_2').order_by('nom')},
            {'nom': 'Groupe 3', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_3').order_by('nom')},
            {'nom': 'Groupe 4', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_4').order_by('nom')},
            {'nom': 'Groupe 5', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_5').order_by('nom')},
            {'nom': 'Groupe 6', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_6').order_by('nom')},
        ]
    elif type_enseignement == 'general':
        groupes_definition = [
            {'nom': 'Groupe 1', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_1').order_by('nom')},
            {'nom': 'Groupe 2', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_2').order_by('nom')},
            {'nom': 'Groupe 3', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_3').order_by('nom')},
        ]

    eleves_data = []
    moyennes_eleves = []

    for eleve in eleves:
        eleve_groupes = []
        total_notes = 0
        total_coefficients = 0
        seq1_moyenne = 0
        seq2_moyenne = 0

        absences_seq1 = Absence.objects.filter(eleve=eleve, classe=classe, sequence='Seq1').aggregate(total_absences=Sum('total'))['total_absences'] or 0
        absences_seq2 = Absence.objects.filter(eleve=eleve, classe=classe, sequence='Seq2').aggregate(total_absences=Sum('total'))['total_absences'] or 0
        absences_non_justifiees = int(absences_seq1) + int(absences_seq2)

        for groupe in groupes_definition:
            matieres_groupes = []

            for matiere in groupe['matieres']:
                seq1_note = Note.objects.filter(eleve=eleve, matiere=matiere, sequence='Seq1').first()
                seq2_note = Note.objects.filter(eleve=eleve, matiere=matiere, sequence='Seq2').first()

                moyenne_trimestrielle = (
                    ((seq1_note.note if seq1_note else 0) + (seq2_note.note if seq2_note else 0)) / 2
                    if seq1_note and seq2_note else (seq1_note.note if seq1_note else (seq2_note.note if seq2_note else 0))
                )

                total_notes += moyenne_trimestrielle * matiere.coefficient
                total_coefficients += matiere.coefficient

                if seq1_note:
                    seq1_moyenne += seq1_note.note * matiere.coefficient
                if seq2_note:
                    seq2_moyenne += seq2_note.note * matiere.coefficient

                classement_matiere = Note.objects.filter(classe=classe, matiere=matiere).values('eleve').annotate(
                    moyenne_matiere=Avg('note')).order_by('-moyenne_matiere')

                rang = next((index + 1 for index, item in enumerate(classement_matiere) if item['eleve'] == eleve.id), None)

                mgc = Note.objects.filter(classe=classe, matiere=matiere).aggregate(moyenne_classe=Avg('note'))['moyenne_classe'] or 0

                appreciation = "Non Acquis" if moyenne_trimestrielle < 10 else "En cours d'acquisition" if moyenne_trimestrielle < 13 else "Acquis"

                matieres_groupes.append({
                    'nom': matiere.nom,
                    'seq1_note': seq1_note.note if seq1_note else '',
                    'seq2_note': seq2_note.note if seq2_note else '',
                    'moyenne': round(moyenne_trimestrielle, 2),
                    'coefficient': matiere.coefficient,
                    'total': round(moyenne_trimestrielle * matiere.coefficient, 2),
                    'rang': rang,
                    'mgc': round(mgc, 2),
                    'min': Note.objects.filter(classe=classe, matiere=matiere).aggregate(Min('note'))['note__min'],
                    'max': Note.objects.filter(classe=classe, matiere=matiere).aggregate(Max('note'))['note__max'],
                    'appreciation': appreciation,
                    'enseignant': matiere.enseignant.nom if matiere.enseignant else '',
                })

            groupe_total_coefficient = sum(m['coefficient'] for m in matieres_groupes)
            groupe_total = sum(m['total'] for m in matieres_groupes)
            groupe_moyenne = groupe_total / groupe_total_coefficient if groupe_total_coefficient else 0

            eleve_groupes.append({
                'nom': groupe['nom'],
                'matieres': matieres_groupes,
                'total_coefficient': groupe_total_coefficient,
                'total': groupe_total,
                'moyenne': round(groupe_moyenne, 2),
            })

        moyenne_generale_eleve = round(total_notes / total_coefficients, 2) if total_coefficients > 0 else 0
        moyennes_eleves.append({'moyenne': moyenne_generale_eleve, 'eleve': eleve})

        appreciation_travail = "Non Acquis" if moyenne_generale_eleve < 10 else "En cours d'acquisition" if moyenne_generale_eleve < 13 else "Acquis"

        eleves_data.append({
            'eleve': eleve,
            'groupes': eleve_groupes,
            'moyenne_generale': moyenne_generale_eleve,
            'absences_seq1': absences_seq1,  # Ajout des absences non justifiées de Seq1
            'absences_seq2': absences_seq2, 
            'absences_non_justifiees': absences_non_justifiees,
            'seq1_moyenne': round(seq1_moyenne / total_coefficients, 2),
            'seq2_moyenne': round(seq2_moyenne / total_coefficients, 2),
            'total_points': total_notes,
            'total_coefficients': total_coefficients,
            'appreciation_travail': appreciation_travail,
        })

    # Tri des élèves par moyenne en ordre décroissant pour le calcul du rang
    moyennes_eleves_sorted = sorted(moyennes_eleves, key=lambda x: x['moyenne'], reverse=True)

    # Attribution des rangs en tenant compte des moyennes exactes
    for rank, eleve in enumerate(moyennes_eleves_sorted, start=1):
        for data in eleves_data:
            if data['eleve'] == eleve['eleve']:
                data['rang'] = rank
                break

    moyenne_classe = round(sum(e['moyenne'] for e in moyennes_eleves) / len(moyennes_eleves), 2) if moyennes_eleves else 0
    variance = sum((e['moyenne'] - moyenne_classe) ** 2 for e in moyennes_eleves) / len(moyennes_eleves) if moyennes_eleves else 0
    ecart_type = math.sqrt(variance)

    stats_classe_trimestre = {
        'moyenne_generale': moyenne_classe,
        'moyenne_dernier': min(e['moyenne'] for e in moyennes_eleves) if moyennes_eleves else 0,
        'moyenne_premier': max(e['moyenne'] for e in moyennes_eleves) if moyennes_eleves else 0,
        'taux_reussite': len([e for e in moyennes_eleves if e['moyenne'] >= 10]) / len(moyennes_eleves) * 100 if moyennes_eleves else 0,
        'nombre_moyennes': len([e for e in moyennes_eleves if e['moyenne'] >= 10]),
        'ecart_type': round(ecart_type, 2),
    }

    return render(request, 'bulletins/afficher_bulletins_trimestriels.html', {
        'classe': classe,
        'eleves_data': eleves_data,
        'profil_classe': stats_classe_trimestre,
        'parametres': parametres,
    })

@login_required
def afficher_bulletins_sequence1(request, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)
    eleves = Eleve.objects.filter(classe_actuelle=classe).order_by('nom')
    parametres = ParametresEtablissement.objects.first()

    type_enseignement = parametres.type_enseignement if parametres else None

    groupes_definition = []
    if type_enseignement == 'technique':
        groupes_definition = [
            {'nom': 'Enseignement Général', 'matieres': Matiere.objects.filter(classe=classe, groupe='enseignement_general').order_by('nom')},
            {'nom': 'Enseignement Professionnel', 'matieres': Matiere.objects.filter(classe=classe, groupe='enseignement_professionnel').order_by('nom')},
            {'nom': 'Enseignement Divers', 'matieres': Matiere.objects.filter(classe=classe, groupe='enseignement_divers').order_by('nom')},
        ]
    elif type_enseignement == 'bilingue':
        groupes_definition = [
            {'nom': 'Groupe 1', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_1').order_by('nom')},
            {'nom': 'Groupe 2', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_2').order_by('nom')},
            {'nom': 'Groupe 3', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_3').order_by('nom')},
        ]
    elif type_enseignement == 'general':
        groupes_definition = [
            {'nom': 'Groupe 1', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_1').order_by('nom')},
            {'nom': 'Groupe 2', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_2').order_by('nom')},
            {'nom': 'Groupe 3', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_3').order_by('nom')},
        ]

    eleves_data = []
    moyennes_eleves = []

    for eleve in eleves:
        eleve_groupes = []
        total_notes = 0
        total_coefficients = 0

        absences_seq1 = Absence.objects.filter(eleve=eleve, classe=classe, sequence='Seq1').aggregate(total_absences=Sum('total'))['total_absences'] or 0

        for groupe in groupes_definition:
            matieres_groupes = []
            groupe_total_notes = 0
            groupe_total_coefficients = 0

            for matiere in groupe['matieres']:
                seq1_note = Note.objects.filter(eleve=eleve, matiere=matiere, sequence='Seq1').first()

                # Vérification si la matière est complète ou non
                if not seq1_note or seq1_note.note == 0 or seq1_note.note == "":
                    continue  # Si la matière est incomplète, on la saute

                moyenne_sequence = seq1_note.note if seq1_note else 0

                groupe_total_notes += moyenne_sequence * matiere.coefficient
                groupe_total_coefficients += matiere.coefficient

                total_notes += moyenne_sequence * matiere.coefficient
                total_coefficients += matiere.coefficient

                classement_matiere = Note.objects.filter(classe=classe, matiere=matiere, sequence='Seq1').values('eleve').annotate(
                    moyenne_matiere=Avg('note')).order_by('-moyenne_matiere')

                rang = next((index + 1 for index, item in enumerate(classement_matiere) if item['eleve'] == eleve.id), None)

                mgc = Note.objects.filter(classe=classe, matiere=matiere, sequence='Seq1').aggregate(moyenne_classe=Avg('note'))['moyenne_classe'] or 0

                appreciation = "Non Acquis" if moyenne_sequence < 10 else "En cours d'acquisition" if moyenne_sequence < 13 else "Acquis"

                matieres_groupes.append({
                    'nom': matiere.nom,
                    'seq1_note': moyenne_sequence,
                    'coefficient': matiere.coefficient,
                    'total': round(moyenne_sequence * matiere.coefficient, 2),
                    'rang': rang,
                    'mgc': round(mgc, 2),
                    'min': Note.objects.filter(classe=classe, matiere=matiere, sequence='Seq1').aggregate(Min('note'))['note__min'],
                    'max': Note.objects.filter(classe=classe, matiere=matiere, sequence='Seq1').aggregate(Max('note'))['note__max'],
                    'appreciation': appreciation,
                    'enseignant': matiere.enseignant.nom if matiere.enseignant else '',
                })

            groupe_moyenne = round(groupe_total_notes / groupe_total_coefficients, 2) if groupe_total_coefficients else 0

            eleve_groupes.append({
                'nom': groupe['nom'],
                'matieres': matieres_groupes,
                'total_coefficient': groupe_total_coefficients,
                'total': groupe_total_notes,
                'moyenne': groupe_moyenne,
            })

        moyenne_generale_eleve = round(total_notes / total_coefficients, 2) if total_coefficients > 0 else 0
        moyennes_eleves.append({'moyenne': moyenne_generale_eleve, 'eleve': eleve})

        appreciation_travail = "Non Acquis" if moyenne_generale_eleve < 10 else "En cours d'acquisition" if moyenne_generale_eleve < 13 else "Acquis"

        eleves_data.append({
            'eleve': eleve,
            'groupes': eleve_groupes,
            'moyenne_generale': moyenne_generale_eleve,
            'absences_seq1': absences_seq1,
            'total_points': total_notes,
            'total_coefficients': total_coefficients,
            'appreciation_travail': appreciation_travail,
        })

    # Tri des élèves par moyenne en ordre décroissant pour le calcul du rang
    moyennes_eleves_sorted = sorted(moyennes_eleves, key=lambda x: x['moyenne'], reverse=True)

    # Attribution des rangs en tenant compte des moyennes exactes
    for rank, eleve in enumerate(moyennes_eleves_sorted, start=1):
        for data in eleves_data:
            if data['eleve'] == eleve['eleve']:
                data['rang'] = rank
                break

    moyenne_classe = round(sum(e['moyenne'] for e in moyennes_eleves) / len(moyennes_eleves), 2) if moyennes_eleves else 0
    variance = sum((e['moyenne'] - moyenne_classe) ** 2 for e in moyennes_eleves) / len(moyennes_eleves) if moyennes_eleves else 0
    ecart_type = round(math.sqrt(variance), 2)

    stats_classe_sequence = {
        'moyenne_generale': moyenne_classe,
        'moyenne_dernier': min(e['moyenne'] for e in moyennes_eleves) if moyennes_eleves else 0,
        'moyenne_premier': max(e['moyenne'] for e in moyennes_eleves) if moyennes_eleves else 0,
        'taux_reussite': len([e for e in moyennes_eleves if e['moyenne'] >= 10]) / len(moyennes_eleves) * 100 if moyennes_eleves else 0,
        'nombre_moyennes': len([e for e in moyennes_eleves if e['moyenne'] >= 10]),
        'ecart_type': ecart_type,
    }

    return render(request, 'bulletins/afficher_bulletins_sequence1.html', {
        'classe': classe,
        'eleves_data': eleves_data,
        'profil_classe': stats_classe_sequence,
        'parametres': parametres,
    })


@login_required
def afficher_bulletins_sequence2(request, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)
    eleves = Eleve.objects.filter(classe_actuelle=classe).order_by('nom')
    parametres = ParametresEtablissement.objects.first()

    type_enseignement = parametres.type_enseignement if parametres else None

    groupes_definition = []
    if type_enseignement == 'technique':
        groupes_definition = [
            {'nom': 'Enseignement Général', 'matieres': Matiere.objects.filter(classe=classe, groupe='enseignement_general').order_by('nom')},
            {'nom': 'Enseignement Professionnel', 'matieres': Matiere.objects.filter(classe=classe, groupe='enseignement_professionnel').order_by('nom')},
            {'nom': 'Enseignement Divers', 'matieres': Matiere.objects.filter(classe=classe, groupe='enseignement_divers').order_by('nom')},
        ]
    elif type_enseignement == 'bilingue':
        groupes_definition = [
            {'nom': 'Groupe 1', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_1').order_by('nom')},
            {'nom': 'Groupe 2', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_2').order_by('nom')},
            {'nom': 'Groupe 3', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_3').order_by('nom')},
        ]
    elif type_enseignement == 'general':
        groupes_definition = [
            {'nom': 'Groupe 1', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_1').order_by('nom')},
            {'nom': 'Groupe 2', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_2').order_by('nom')},
            {'nom': 'Groupe 3', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_3').order_by('nom')},
        ]

    eleves_data = []
    moyennes_eleves = []

    for eleve in eleves:
        eleve_groupes = []
        total_notes = 0
        total_coefficients = 0

        absences_seq2 = Absence.objects.filter(eleve=eleve, classe=classe, sequence='Seq2').aggregate(total_absences=Sum('total'))['total_absences'] or 0

        for groupe in groupes_definition:
            matieres_groupes = []
            groupe_total_notes = 0
            groupe_total_coefficients = 0

            for matiere in groupe['matieres']:
                seq2_note = Note.objects.filter(eleve=eleve, matiere=matiere, sequence='Seq2').first()

                # Vérification si la matière est complète ou non
                if not seq2_note or seq2_note.note == 0 or seq2_note.note == "":
                    continue  # Si la matière est incomplète, on la saute

                moyenne_sequence = seq2_note.note if seq2_note else 0

                groupe_total_notes += moyenne_sequence * matiere.coefficient
                groupe_total_coefficients += matiere.coefficient

                total_notes += moyenne_sequence * matiere.coefficient
                total_coefficients += matiere.coefficient

                classement_matiere = Note.objects.filter(classe=classe, matiere=matiere, sequence='Seq2').values('eleve').annotate(
                    moyenne_matiere=Avg('note')).order_by('-moyenne_matiere')

                rang = next((index + 1 for index, item in enumerate(classement_matiere) if item['eleve'] == eleve.id), None)

                mgc = Note.objects.filter(classe=classe, matiere=matiere, sequence='Seq2').aggregate(moyenne_classe=Avg('note'))['moyenne_classe'] or 0

                appreciation = "Non Acquis" if moyenne_sequence < 10 else "En cours d'acquisition" if moyenne_sequence < 13 else "Acquis"

                matieres_groupes.append({
                    'nom': matiere.nom,
                    'seq2_note': moyenne_sequence,
                    'coefficient': matiere.coefficient,
                    'total': round(moyenne_sequence * matiere.coefficient, 2),
                    'rang': rang,
                    'mgc': round(mgc, 2),
                    'min': Note.objects.filter(classe=classe, matiere=matiere, sequence='Seq2').aggregate(Min('note'))['note__min'],
                    'max': Note.objects.filter(classe=classe, matiere=matiere, sequence='Seq2').aggregate(Max('note'))['note__max'],
                    'appreciation': appreciation,
                    'enseignant': matiere.enseignant.nom if matiere.enseignant else '',
                })

            groupe_moyenne = round(groupe_total_notes / groupe_total_coefficients, 2) if groupe_total_coefficients else 0

            eleve_groupes.append({
                'nom': groupe['nom'],
                'matieres': matieres_groupes,
                'total_coefficient': groupe_total_coefficients,
                'total': groupe_total_notes,
                'moyenne': groupe_moyenne,
            })

        moyenne_generale_eleve = round(total_notes / total_coefficients, 2) if total_coefficients > 0 else 0
        moyennes_eleves.append({'moyenne': moyenne_generale_eleve, 'eleve': eleve})

        appreciation_travail = "Non Acquis" if moyenne_generale_eleve < 10 else "En cours d'acquisition" if moyenne_generale_eleve < 13 else "Acquis"

        eleves_data.append({
            'eleve': eleve,
            'groupes': eleve_groupes,
            'moyenne_generale': moyenne_generale_eleve,
            'absences_seq2': absences_seq2,
            'total_points': total_notes,
            'total_coefficients': total_coefficients,
            'appreciation_travail': appreciation_travail,
        })

    # Tri des élèves par moyenne en ordre décroissant pour le calcul du rang
    moyennes_eleves_sorted = sorted(moyennes_eleves, key=lambda x: x['moyenne'], reverse=True)

    # Attribution des rangs en tenant compte des moyennes exactes
    for rank, eleve in enumerate(moyennes_eleves_sorted, start=1):
        for data in eleves_data:
            if data['eleve'] == eleve['eleve']:
                data['rang'] = rank
                break

    moyenne_classe = round(sum(e['moyenne'] for e in moyennes_eleves) / len(moyennes_eleves), 2) if moyennes_eleves else 0
    variance = sum((e['moyenne'] - moyenne_classe) ** 2 for e in moyennes_eleves) / len(moyennes_eleves) if moyennes_eleves else 0
    ecart_type = round(math.sqrt(variance), 2)

    stats_classe_sequence = {
        'moyenne_generale': moyenne_classe,
        'moyenne_dernier': min(e['moyenne'] for e in moyennes_eleves) if moyennes_eleves else 0,
        'moyenne_premier': max(e['moyenne'] for e in moyennes_eleves) if moyennes_eleves else 0,
        'taux_reussite': len([e for e in moyennes_eleves if e['moyenne'] >= 10]) / len(moyennes_eleves) * 100 if moyennes_eleves else 0,
        'nombre_moyennes': len([e for e in moyennes_eleves if e['moyenne'] >= 10]),
        'ecart_type': ecart_type,
    }

    return render(request, 'bulletins/afficher_bulletins_sequence2.html', {
        'classe': classe,
        'eleves_data': eleves_data,
        'profil_classe': stats_classe_sequence,
        'parametres': parametres,
    })


@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def liste_classes_par_sequence(request):
    form = SequenceSelectionForm(request.GET)
    sequence = request.GET.get('sequence')
    classes = Classe.objects.all()
    context = {
        'form': form,
        'sequence': sequence,
        'classes': classes,
    }
    return render(request, 'notes/liste_classes_par_sequence.html', context)


@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def liste_matieres_incompletes_par_classe(request, classe_id, sequence):
    classe = get_object_or_404(Classe, id=classe_id)
    matieres_incompletes = []

    # Récupérer toutes les matières de la classe
    matieres = Matiere.objects.filter(classe=classe)

    for matiere in matieres:
        # Récupérer les notes pour cette matière et cette séquence
        notes = Note.objects.filter(matiere=matiere, sequence=sequence)
        
        # Vérifier si la matière est incomplète
        matiere_incomplete = any(note.note == "" or note.note == 0 for note in notes) or notes.count() < Eleve.objects.filter(classe_actuelle=classe).count()

        if matiere_incomplete:
            matieres_incompletes.append({
                'matiere': matiere,
                'sequence': sequence,
                'classe': classe
            })

    return render(request, 'notes/liste_matieres_incompletes_par_classe.html', {
        'classe': classe,
        'sequence': sequence,
        'matieres_incompletes': matieres_incompletes,
    })

@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def imprimer_bordereau_notes(request, classe_id, sequence):
    # Récupération de la classe et des élèves associés
    classe = get_object_or_404(Classe, id=classe_id)
    eleves = Eleve.objects.filter(classe_actuelle=classe).order_by('nom')
    parametres = ParametresEtablissement.objects.first()

    # Définition des groupes et matières en fonction du type d'enseignement
    groupes_definition = []
    if parametres.type_enseignement == 'technique':
        groupes_definition = [
            {'nom': 'Enseignement Général', 'matieres': Matiere.objects.filter(classe=classe, groupe='enseignement_general').order_by('nom')},
            {'nom': 'Enseignement Professionnel', 'matieres': Matiere.objects.filter(classe=classe, groupe='enseignement_professionnel').order_by('nom')},
            {'nom': 'Enseignement Divers', 'matieres': Matiere.objects.filter(classe=classe, groupe='enseignement_divers').order_by('nom')},
        ]
    elif parametres.type_enseignement == 'bilingue':
        groupes_definition = [
            {'nom': 'Groupe 1', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_1').order_by('nom')},
            {'nom': 'Groupe 2', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_2').order_by('nom')},
            {'nom': 'Groupe 3', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_3').order_by('nom')},
        ]
    elif parametres.type_enseignement == 'general':
        groupes_definition = [
            {'nom': 'Groupe 1', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_1').order_by('nom')},
            {'nom': 'Groupe 2', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_2').order_by('nom')},
            {'nom': 'Groupe 3', 'matieres': Matiere.objects.filter(classe=classe, groupe='groupe_3').order_by('nom')},
        ]

    # Préparation des données pour chaque élève
    eleves_data = []
    for eleve in eleves:
        notes_par_matiere = []
        for groupe in groupes_definition:
            for matiere in groupe['matieres']:
                # Récupérer la note de l'élève pour chaque matière dans la séquence donnée
                note = Note.objects.filter(eleve=eleve, matiere=matiere, sequence=sequence).first()
                if note:
                    notes_par_matiere.append(note.note)
                else:
                    notes_par_matiere.append('-')  # Afficher un tiret si la note n'existe pas
        eleves_data.append({
            'eleve': eleve,
            'notes_par_matiere': notes_par_matiere,
        })

    context = {
        'classe': classe,
        'eleves_data': eleves_data,
        'groupes_definition': groupes_definition,
        'parametres': parametres,
        'sequence': sequence
    }

    # Génération du PDF à partir du template
    template_path = 'notes/bordereau_notes_pdf.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="Bordereau_Notes_{classe.nom}_Seq{sequence}.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    # Utilisation de pisa pour créer le PDF
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse("Une erreur s'est produite lors de la génération du PDF", status=400)
    return response

@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def bordereau_par_sequence(request):
    form = SequenceSelectionForm(request.GET)
    sequence = request.GET.get('sequence')
    classes = Classe.objects.all()
    context = {
        'form': form,
        'sequence': sequence,
        'classes': classes,
    }
    return render(request, 'notes/bordereau_par_sequence.html', context)

def calcul_statistiques_matiere_trimestrielle(classe, matiere, sequences):
    # Récupérer les notes pour les séquences spécifiées
    notes = Note.objects.filter(classe=classe, matiere=matiere, sequence__in=sequences)

    total_eleves = notes.values('eleve').distinct().count()
    nb_garcons = notes.filter(eleve__sexe='Masculin').values('eleve').distinct().count()
    nb_filles = notes.filter(eleve__sexe='Feminin').values('eleve').distinct().count()

    # Calcul des moyennes
    moyenne_classe = notes.aggregate(Avg('note'))['note__avg'] or 0
    max_note = notes.aggregate(Max('note'))['note__max'] or 0
    min_note = notes.aggregate(Min('note'))['note__min'] or 0

    # Calcul des élèves ayant la moyenne
    nb_garcons_moyenne = notes.filter(eleve__sexe='Masculin', note__gte=10).values('eleve').distinct().count()
    nb_filles_moyenne = notes.filter(eleve__sexe='Feminin', note__gte=10).values('eleve').distinct().count()
    nb_eleves_moyenne = nb_garcons_moyenne + nb_filles_moyenne

    # Calcul des pourcentages de réussite
    pourcentage_reussite_garcons = (nb_garcons_moyenne / nb_garcons) * 100 if nb_garcons > 0 else 0
    pourcentage_reussite_filles = (nb_filles_moyenne / nb_filles) * 100 if nb_filles > 0 else 0
    pourcentage_reussite_total = (nb_eleves_moyenne / total_eleves) * 100 if total_eleves > 0 else 0

    # Calcul des élèves ayant la sous-moyenne
    nb_garcons_sous_moyenne = nb_garcons - nb_garcons_moyenne
    nb_filles_sous_moyenne = nb_filles - nb_filles_moyenne
    nb_eleves_sous_moyenne = total_eleves - nb_eleves_moyenne

    # Calcul des pourcentages d'échec
    pourcentage_echec_garcons = 100 - pourcentage_reussite_garcons if nb_garcons > 0 else 0
    pourcentage_echec_filles = 100 - pourcentage_reussite_filles if nb_filles > 0 else 0
    pourcentage_echec_total = 100 - pourcentage_reussite_total if total_eleves > 0 else 0

    # Calcul de l'écart-type
    variance = sum((note.note - moyenne_classe) ** 2 for note in notes) / total_eleves if total_eleves > 0 else 0
    ecart_type = round(math.sqrt(variance), 2)

    stats_classe_trimestre = {
        'total_eleves': total_eleves,
        'total_garcons': nb_garcons,
        'total_filles': nb_filles,
        'moyenne_classe': round(moyenne_classe, 2),
        'max_note': round(max_note, 2),
        'min_note': round(min_note, 2),
        'nb_garcons_moyenne': nb_garcons_moyenne,
        'nb_filles_moyenne': nb_filles_moyenne,
        'nb_eleves_moyenne': nb_eleves_moyenne,
        'nb_garcons_sous_moyenne': nb_garcons_sous_moyenne,
        'nb_filles_sous_moyenne': nb_filles_sous_moyenne,
        'nb_eleves_sous_moyenne': nb_eleves_sous_moyenne,
        'pourcentage_reussite_garcons': round(pourcentage_reussite_garcons, 2),
        'pourcentage_reussite_filles': round(pourcentage_reussite_filles, 2),
        'pourcentage_reussite_total': round(pourcentage_reussite_total, 2),
        'pourcentage_echec_garcons': round(pourcentage_echec_garcons, 2),
        'pourcentage_echec_filles': round(pourcentage_echec_filles, 2),
        'pourcentage_echec_total': round(pourcentage_echec_total, 2),
        'ecart_type': ecart_type,
    }

    return stats_classe_trimestre




@login_required
@role_required(allowed_roles=['AP', 'SG', 'Admin_'])
def statistiques_trimestrielles_departement(request, trimestre):
    utilisateur = request.user.profilutilisateur

    # Déterminer les départements à afficher en fonction du rôle de l'utilisateur
    if utilisateur.role == 'Admin_':
        departements = Departement.objects.all()
    elif utilisateur.role == 'SG':
        departements = Departement.objects.filter(utilisateur_sg=utilisateur)
    elif utilisateur.role == 'AP':
        departements = Departement.objects.filter(chef_departement=utilisateur)

    if not departements.exists():
        messages.error(request, "Vous n'êtes responsable d'aucun département.")
        return redirect('home')

    departement_id = request.GET.get('departement_id')
    if departement_id:
        departement = get_object_or_404(Departement, id=departement_id)
    else:
        departement = departements.first()

    if trimestre == 'T1':
        sequences = ['Seq1', 'Seq2']
    elif trimestre == 'T2':
        sequences = ['Seq3', 'Seq4']
    elif trimestre == 'T3':
        sequences = ['Seq5']
    else:
        messages.error(request, "Trimestre invalide")
        return redirect('menu_gestion_trimestres')

    matieres = Matiere.objects.filter(departement=departement)

    statistiques = []
    stats_globales = {
        'total_eleves': 0,
        'total_garcons': 0,
        'total_filles': 0,
        'total_garcons_moyenne': 0,
        'total_filles_moyenne': 0,
        'total_eleves_moyenne': 0,
        'moyenne_generale_departement': 0,
        'pourcentage_reussite_garcons': 0,
        'pourcentage_reussite_filles': 0,
        'pourcentage_reussite_total': 0,
        'ecart_type_global': 0,
    }

    total_moyennes = 0
    nombre_notes = 0
    variances = []

    for matiere in matieres:
        classes = Classe.objects.filter(matieres=matiere).distinct()
        stats_par_classe = []

        for classe in classes:
            stats_classe = calcul_statistiques_matiere_trimestrielle(classe, matiere, sequences)
            stats_par_classe.append({
                'classe': classe,
                'stats': stats_classe,
            })

            # Accumuler les statistiques globales
            stats_globales['total_eleves'] += stats_classe['total_eleves']
            stats_globales['total_garcons'] += stats_classe['total_garcons']
            stats_globales['total_filles'] += stats_classe['total_filles']
            stats_globales['total_garcons_moyenne'] += stats_classe['nb_garcons_moyenne']
            stats_globales['total_filles_moyenne'] += stats_classe['nb_filles_moyenne']
            stats_globales['total_eleves_moyenne'] += stats_classe['nb_eleves_moyenne']

            total_moyennes += stats_classe['moyenne_classe'] * stats_classe['total_eleves']
            nombre_notes += stats_classe['total_eleves']
            variances.append((stats_classe['moyenne_classe'], stats_classe['ecart_type'], stats_classe['total_eleves']))

        statistiques.append({
            'matiere': matiere,
            'stats_par_classe': stats_par_classe,
        })

    if nombre_notes > 0:
        stats_globales['moyenne_generale_departement'] = round(total_moyennes / nombre_notes, 2)

    # Calcul de l'écart-type global
    if nombre_notes > 0:
        variance_globale = sum(
            ((moyenne_classe - stats_globales['moyenne_generale_departement']) ** 2) * total_eleves
            for moyenne_classe, ecart_type, total_eleves in variances
        ) / nombre_notes
        stats_globales['ecart_type_global'] = round(math.sqrt(variance_globale), 2)

    if stats_globales['total_garcons'] > 0:
        stats_globales['pourcentage_reussite_garcons'] = round((stats_globales['total_garcons_moyenne'] / stats_globales['total_garcons']) * 100, 2)

    if stats_globales['total_filles'] > 0:
        stats_globales['pourcentage_reussite_filles'] = round((stats_globales['total_filles_moyenne'] / stats_globales['total_filles']) * 100, 2)

    if stats_globales['total_eleves'] > 0:
        stats_globales['pourcentage_reussite_total'] = round((stats_globales['total_eleves_moyenne'] / stats_globales['total_eleves']) * 100, 2)

    context = {
        'departements': departements,
        'selected_departement': departement,
        'trimestre': trimestre,
        'statistiques': statistiques,
        'stats_globales': stats_globales,
    }

    return render(request, 'notes/statistiques_trimestrielles_departement.html', context)

