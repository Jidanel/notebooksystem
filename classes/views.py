from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import *
from .forms import *
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.core.paginator import Paginator
from utilisateurs.decorators import *
from utilisateurs.views import *

@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def liste_classes(request):
    query = request.GET.get('q')
    classes = Classe.objects.all().order_by('nom')

    if query:
        classes = classes.filter(nom__icontains=query)

    paginator = Paginator(classes, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'classes/liste_classes.html', {'page_obj': page_obj, 'query': query})

@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def ajouter_classe(request):
    if request.method == 'POST':
        form = ClasseForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Classe ajoutée avec succès.")
            return redirect('liste_classes')
    else:
        form = ClasseForm()
    return render(request, 'classes/ajouter_classe.html', {'form': form})

@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def modifier_classe(request, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)
    if request.method == 'POST':
        form = ClasseForm(request.POST, instance=classe)
        if form.is_valid():
            form.save()
            messages.success(request, "Classe modifiée avec succès.")
            return redirect('liste_classes')
    else:
        form = ClasseForm(instance=classe)
    return render(request, 'classes/modifier_classe.html', {'form': form})

@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def confirmer_suppression_classe(request, classe_id):
    return supprimer_objet_securise(
        request, 
        model=Classe, 
        pk=classe_id, 
        redirect_url='liste_classes'
    )

@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def imprimer_classe(request, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)
    
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = f'inline; filename=classe_{classe.nom}.pdf'
    
    p = canvas.Canvas(response, pagesize=letter)
    y_position = 750
    p.drawString(100, y_position, f"Classe: {classe.nom}")
    y_position -= 30
    p.drawString(100, y_position, f"Code: {classe.code}")
    y_position -= 30
    if classe.enseignant_titulaire:
        p.drawString(100, y_position, f"Enseignant Titulaire: {classe.enseignant_titulaire.username}")
    else:
        p.drawString(100, y_position, "Enseignant Titulaire: Non assigné")
    y_position -= 30

    p.drawString(100, y_position, "Liste des Élèves:")
    y_position -= 30
    for eleve in classe.eleves.all():
        p.drawString(100, y_position, f"- {eleve.nom} {eleve.prenom}")
        y_position -= 20
    
    p.showPage()
    p.save()
    
    return response

@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def details_classe(request, classe_id):
    classe = get_object_or_404(Classe, id=classe_id)
    
    # Calcul des différents nombres
    nombre_eleves = classe.eleves.count()
    nombre_garcons = classe.eleves.filter(sexe='Masculin').count()
    nombre_filles = classe.eleves.filter(sexe='Feminin').count()
    nombre_redoublants = classe.eleves.filter(statut='Redoublant').count()
    nombre_nouveaux = classe.eleves.filter(statut='Nouveau').count()
    
    context = {
        'classe': classe,
        'nombre_eleves': nombre_eleves,
        'nombre_garcons': nombre_garcons,
        'nombre_filles': nombre_filles,
        'nombre_redoublants': nombre_redoublants,
        'nombre_nouveaux': nombre_nouveaux,
    }
    
    return render(request, 'classes/details_classe.html', context)


@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def menu_gestion_classes(request):
    return render(request, 'classes/menu_gestion_classes.html')