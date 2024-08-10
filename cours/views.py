from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Matiere
from .forms import MatiereForm
from utilisateurs.models import *

@login_required
def liste_matieres(request):
    query = request.GET.get('q')
    matieres = Matiere.objects.all().order_by('nom')

    if query:
        matieres = matieres.filter(nom__icontains=query)

    paginator = Paginator(matieres, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cours/liste_matieres.html', {'page_obj': page_obj, 'query': query})

@login_required
def ajouter_matiere(request):
    if request.method == 'POST':
        form = MatiereForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Matière ajoutée avec succès.")
        else:
            messages.error(request, "Erreur lors de l'ajout de la matière. Veuillez vérifier les informations fournies.")
    else:
        form = MatiereForm()

    return render(request, 'cours/ajouter_matiere.html', {'form': form})

@login_required
def filtrer_enseignants_par_departement(request):
    departement_id = request.GET.get('departement')
    form = MatiereForm(request.GET)
    if departement_id:
        form.fields['enseignant'].queryset = ProfilUtilisateur.objects.filter(
            enseignantdepartement__departement_id=departement_id
        ).order_by('nom')
    return render(request, 'cours/ajouter_matiere.html', {'form': form})

@login_required
def modifier_matiere(request, matiere_id):
    matiere = get_object_or_404(Matiere, id=matiere_id)
    if request.method == 'POST':
        form = MatiereForm(request.POST, instance=matiere)
        if form.is_valid():
            form.save()
            messages.success(request, "Matière modifiée avec succès.")
            return redirect('liste_matieres')
    else:
        form = MatiereForm(instance=matiere)
        if 'departement' in request.GET:
            departement_id = request.GET.get('departement')
            form.fields['enseignant'].queryset = ProfilUtilisateur.objects.filter(
                enseignantdepartement__departement_id=departement_id
            ).order_by('nom')
        else:
            form.fields['enseignant'].queryset = ProfilUtilisateur.objects.filter(
                enseignantdepartement__departement_id=matiere.departement.id
            ).order_by('nom')

    return render(request, 'cours/modifier_matiere.html', {'form': form, 'matiere': matiere})

@login_required
def confirmer_suppression_matiere(request, matiere_id):
    matiere = get_object_or_404(Matiere, id=matiere_id)
    if request.method == 'POST':
        matiere.delete()
        messages.success(request, "Matière supprimée avec succès.")
        return redirect('liste_matieres')
    return render(request, 'cours/confirmer_suppression_matiere.html', {'matiere': matiere})

