from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.contrib import messages
from .models import Matiere
from .forms import MatiereForm
from utilisateurs.models import *
from utilisateurs.decorators import *
from utilisateurs.views import *
from parametres.models import *
from classes.models import *
from django.db.models import Sum

@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def liste_matieres(request):
    query = request.GET.get('q')
    matieres = Matiere.objects.select_related('classe', 'departement', 'enseignant').all().order_by('nom')

    if query:
        matieres = matieres.filter(nom__icontains=query)

    paginator = Paginator(matieres, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'cours/liste_matieres.html', {'page_obj': page_obj, 'query': query})

@role_required(allowed_roles=['Admin_', 'SG'])
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

@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def filtrer_enseignants_par_departement(request):
    departement_id = request.GET.get('departement')
    form = MatiereForm(request.GET)
    if departement_id:
        form.fields['enseignant'].queryset = ProfilUtilisateur.objects.filter(
            enseignantdepartement__departement_id=departement_id
        ).order_by('nom')
    return render(request, 'cours/ajouter_matiere.html', {'form': form})

@role_required(allowed_roles=['Admin_', 'SG'])
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

@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def confirmer_suppression_matiere(request, matiere_id):
    return supprimer_objet_securise(
        request, 
        model=Matiere, 
        pk=matiere_id, 
        redirect_url='liste_matieres'
    )

@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def liste_groupes_par_classe(request, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)
    matieres = Matiere.objects.filter(classe=classe).select_related('departement', 'enseignant')

    parametres = ParametresEtablissement.objects.first()
    type_enseignement = parametres.type_enseignement if parametres else None

    groupes_matieres = []

    if type_enseignement == 'technique':
        groupes = [
            {'nom': 'Enseignement Général', 'matieres': matieres.filter(groupe__exact='enseignement_general')},
            {'nom': 'Enseignement Professionnel', 'matieres': matieres.filter(groupe__exact='enseignement_professionnel')},
            {'nom': 'Enseignement Divers', 'matieres': matieres.filter(groupe__exact='enseignement_divers')},
        ]
    elif type_enseignement == 'bilingue':
        groupes = [
            {'nom': 'Groupe 1', 'matieres': matieres.filter(groupe__exact='groupe_1')},
            {'nom': 'Groupe 2', 'matieres': matieres.filter(groupe__exact='groupe_2')},
            {'nom': 'Groupe 3', 'matieres': matieres.filter(groupe__exact='groupe_3')},
            {'nom': 'Groupe 4', 'matieres': matieres.filter(groupe__exact='groupe_4')},
            {'nom': 'Groupe 5', 'matieres': matieres.filter(groupe__exact='groupe_5')},
            {'nom': 'Groupe 6', 'matieres': matieres.filter(groupe__exact='groupe_6')},
        ]
    elif type_enseignement == 'general':
        groupes = [
            {'nom': 'Groupe 1', 'matieres': matieres.filter(groupe__exact='groupe_1')},
            {'nom': 'Groupe 2', 'matieres': matieres.filter(groupe__exact='groupe_2')},
            {'nom': 'Groupe 3', 'matieres': matieres.filter(groupe__exact='groupe_3')},
        ]
    else:
        groupes = []

    for groupe in groupes:
        total_coefficient = groupe['matieres'].aggregate(Sum('coefficient'))['coefficient__sum'] or 0
        groupes_matieres.append({
            'nom': groupe['nom'],
            'matieres': groupe['matieres'],
            'total_coefficient': total_coefficient,
        })

    return render(request, 'cours/liste_groupes_par_classe.html', {
        'classe': classe,
        'groupes_matieres': groupes_matieres,
    })