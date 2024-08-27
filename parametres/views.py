from django.shortcuts import render, redirect
from .forms import ParametresEtablissementForm
from .models import ParametresEtablissement
from django.contrib import messages
from utilisateurs.decorators import *
from django.contrib.auth.decorators import login_required
from utilisateurs.views import *

@login_required
@role_required(allowed_roles=['Admin_', 'SG'])
def gerer_parametres_etablissement(request):
    parametres, created = ParametresEtablissement.objects.get_or_create(id=1)

    if request.method == 'POST':
        form = ParametresEtablissementForm(request.POST, request.FILES, instance=parametres)
        if form.is_valid():
            form.save()
            messages.success(request, "Paramètres de l'établissement mis à jour avec succès.")
            return redirect('home')
    else:
        form = ParametresEtablissementForm(instance=parametres)

    return render(request, 'parametres/gerer_parametres_etablissement.html', {'form': form})

