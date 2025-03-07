# absences/views.py
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from .forms import *
from .models import Absence
from eleves.models import Eleve
from classes.models import Classe
from django.db.models import Q
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from utilisateurs.models import *
from utilisateurs.decorators import *
from parametres.models import *

@login_required
def selection_classe_sequence(request):
    if request.method == 'POST':
        form = ClasseSequenceSelectionForm(request.POST)
        if form.is_valid():
            classe_id = form.cleaned_data['classe'].id
            sequence = form.cleaned_data['sequence']
            return redirect('saisie_absences', classe_id=classe_id, sequence=sequence)
    else:
        form = ClasseSequenceSelectionForm()
    return render(request, 'absences/selection_classe_sequence.html', {'form': form})

@login_required
def saisie_absences(request, classe_id, sequence):
    classe = get_object_or_404(Classe, id=classe_id)
    eleves = Eleve.objects.filter(classe_actuelle=classe).select_related('classe_actuelle').order_by('nom')
    absences_existantes = {absence.eleve.id: absence.absences for absence in Absence.objects.filter(classe=classe, sequence=sequence)}

    if request.method == 'POST':
        all_filled = True
        for eleve in eleves:
            absence_value = request.POST.get(f'absence_{eleve.id}')
            if not absence_value:
                all_filled = False
                break
        if all_filled:
            enseignant = request.user.profilutilisateur
            for eleve in eleves:
                absence_value = request.POST.get(f'absence_{eleve.id}')
                try:
                    absence_value = int(absence_value)
                except ValueError:
                    messages.error(request, "Les valeurs des absences doivent être des nombres entiers.")
                    return redirect('saisie_absences', classe_id=classe_id, sequence=sequence)

                Absence.objects.update_or_create(
                    eleve=eleve,
                    classe=classe,
                    sequence=sequence,
                    defaults={'absences': absence_value, 'enseignant': enseignant}
                )
            messages.success(request, "Les absences ont été enregistrées avec succès.")
            return redirect('menu_gestion_trimestres')
        else:
            messages.error(request, "Veuillez remplir toutes les absences avant d'enregistrer.")

    return render(request, 'absences/saisie_absences.html', {
        'eleves': eleves,
        'classe': classe,
        'sequence': sequence,
        'absences_existantes': absences_existantes
    })

@login_required
def liste_absences_completes(request):
    enseignant = request.user.profilutilisateur
    absences_completes = Absence.objects.filter(enseignant=enseignant).distinct('classe', 'sequence')
    return render(request, 'absences/liste_absences_completes.html', {'absences_completes': absences_completes})

@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def justifier_absences(request, sequence, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)
    eleves = Eleve.objects.filter(classe_actuelle=classe).select_related('classe_actuelle').order_by('nom')
    absences_existantes = {absence.eleve.id: absence for absence in Absence.objects.filter(classe=classe, sequence=sequence)}

    if request.method == 'POST':
        for eleve in eleves:
            absence = absences_existantes.get(eleve.id)
            if absence:
                justification = request.POST.get(f'justification_{eleve.id}', 0)
                try:
                    justification = int(justification)
                except ValueError:
                    justification = 0

                absence.justification = justification
                absence.total = absence.absences - absence.justification
                absence.save()
        messages.success(request, "Les justifications ont été enregistrées avec succès.")
        return redirect('liste_absences_completes')

    return render(request, 'absences/justifier_absences.html', {
        'eleves': eleves,
        'classe': classe,
        'sequence': sequence,
        'absences_existantes': absences_existantes
    })

@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def imprimer_absences(request, sequence, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)
    eleves = Eleve.objects.filter(classe_actuelle=classe).select_related('classe_actuelle').order_by('nom')
    absences = Absence.objects.filter(classe=classe, sequence=sequence).select_related('eleve', 'classe').order_by('eleve__nom')
    
    parametres_etablissement = ParametresEtablissement.objects.first()

    with_justifications = request.GET.get('with_justifications', 'False') == 'True'

    template_path = 'absences/imprimer_absences.html' if with_justifications else 'absences/imprimer_absences_sans_justifications.html'
    
    context = {
        'eleves': eleves,
        'classe': classe,
        'sequence': sequence,
        'absences': absences,
        'with_justifications': with_justifications,
        'parametres_etablissement': parametres_etablissement
    }

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'filename="Absences_{classe.nom}_{sequence}.pdf"'
    template = get_template(template_path)
    html = template.render(context)
    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('We had some errors <pre>' + html + '</pre>')
    return response