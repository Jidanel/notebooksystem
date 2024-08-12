from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import ClasseMatiereSelectionForm
from .models import Note
from eleves.models import Eleve
from classes.models import Classe
from cours.models import Matiere
from utilisateurs.models import *
from django.db.models import Q
from utilisateurs.decorators import *

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
            if not note_value:
                all_filled = False
                break
        if all_filled:
            for eleve in eleves:
                note_value = request.POST.get(f'note_{eleve.id}')
                Note.objects.update_or_create(
                    eleve=eleve,
                    matiere=matiere,
                    sequence=sequence,
                    defaults={'note': note_value, 'classe': classe, 'enseignant': request.user.profilutilisateur, 'completed': True}
                )
            messages.success(request, "Les notes ont été enregistrées avec succès.")
            return redirect('menu_gestion_trimestres')  # Redirigez vers l'URL appropriée
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
