from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *
from .decorators import *
from django.core.paginator import Paginator
from django.db.models import Q
from django.contrib.auth.forms import SetPasswordForm
from django.shortcuts import get_object_or_404
from django.utils.crypto import get_random_string
from .forms import AssignerClasseForm
from parametres.models import *
from django.http import HttpResponse
from xhtml2pdf import pisa  # Pour générer des PDF
from django.template.loader import get_template


@login_required(login_url='login')
def index(request):
    return render(request, 'utilisateurs/home.html')

@login_required(login_url='login')
def profile(request):
    # Vérifiez si l'utilisateur a un profil associé
    try:
        profile = request.user.profilutilisateur
    except ProfilUtilisateur.DoesNotExist:
        # Créez un profil si l'utilisateur n'en a pas
        profile = ProfilUtilisateur.objects.create(utilisateur=request.user)

    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES, instance=profile)
        if form.is_valid():
            form.save()
            username = request.user.username
            messages.success(request, f'{username}, votre profil a été mis à jour.')
            return redirect('profile')
    else:
        form = ProfileForm(instance=profile)
    context = {'form': form}
    return render(request, 'utilisateurs/profile.html', context)

@unauthenticated_user
def login_user(request):
    if request.method == 'POST':
        username_or_matricule = request.POST.get('username_or_matricule')
        password = request.POST.get('password')

        # Authentification par nom d'utilisateur ou matricule
        try:
            user = User.objects.get(username=username_or_matricule)
        except User.DoesNotExist:
            try:
                profile = ProfilUtilisateur.objects.get(matricule=username_or_matricule)
                user = profile.utilisateur
            except ProfilUtilisateur.DoesNotExist:
                user = None

        if user is not None:
            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'{user.username}, vous êtes connecté.')
                return redirect("/")
        messages.error(request, 'Nom d’utilisateur, matricule ou mot de passe incorrect.')
    return render(request, 'utilisateurs/login_page.html')

@unauthenticated_user
def register_user(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Vérifie si le profil existe déjà pour cet utilisateur
            if not ProfilUtilisateur.objects.filter(utilisateur=user).exists():
                ProfilUtilisateur.objects.create(utilisateur=user)
            messages.success(request, 'Votre compte a été créé avec succès.')
            return redirect('login')
        else:
            messages.error(request, 'Identifiants invalides')
    context = {'form': form}
    return render(request, 'utilisateurs/register_page.html', context)


@login_required(login_url='login')
def logout_user(request):
    logout(request)
    messages.success(request, 'Vous vous êtes déconnecté avec succès.')
    return redirect('login')


@login_required(login_url='login')
def previous_view(request):
    # Logique pour le bouton précédent
    return redirect('home')

@login_required(login_url='login')
def next_view(request):
    # Logique pour le bouton suivant
    return redirect('home')

@role_required(allowed_roles=['Admin_', 'AP', 'SG'])
@login_required(login_url='login')
def liste_enseignants(request):
    query = request.GET.get('q')
    enseignants = ProfilUtilisateur.objects.filter(actif=True).order_by('nom').prefetch_related('enseignantdepartement_set__departement')

    if query:
        enseignants = enseignants.filter(
            Q(nom__icontains=query) |
            Q(matricule__icontains=query) |
            Q(role__icontains=query)
        )

 

    paginator = Paginator(enseignants, 10)  # 10 enseignants par page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'query': query,
    }
    return render(request, 'utilisateurs/liste_enseignants.html', context)

@role_required(allowed_roles=['Admin_'])
@login_required(login_url='login')
def assigner_role(request):
    if request.method == 'POST':
        form = RoleAssignmentForm(request.POST)
        if form.is_valid():
            utilisateur_id = request.POST.get('utilisateur')
            utilisateur = User.objects.get(id=utilisateur_id)
            
            try:
                profil = ProfilUtilisateur.objects.get(utilisateur=utilisateur)
            except ProfilUtilisateur.DoesNotExist:
                profil = ProfilUtilisateur(utilisateur=utilisateur)
            
            profil.role = form.cleaned_data['role']
            profil.save()

            # Déconnexion automatique de l'utilisateur
            if utilisateur == request.user:
                logout(request)
                messages.info(request, "Votre rôle a changé. Veuillez vous reconnecter.")
                return redirect('login')

            messages.success(request, f"Le rôle de {utilisateur.username} a été mis à jour avec succès.")
            return redirect('assigner_role')
    else:
        form = RoleAssignmentForm()
    
    utilisateurs = User.objects.all()
    context = {'form': form, 'utilisateurs': utilisateurs}
    return render(request, 'utilisateurs/assigner_role.html', context)

@role_required(allowed_roles=['Admin_', 'AP', 'SG'])
@login_required(login_url='login')
def menu_gestion_enseignants(request):
    return render(request, 'utilisateurs/menu_gestion_enseignants.html')

@role_required(allowed_roles=['Admin_', 'SG'])
@login_required(login_url='login')
def reset_password(request, user_id):
    utilisateur = get_object_or_404(User, id=user_id)
    profil = get_object_or_404(ProfilUtilisateur, utilisateur=utilisateur)

    if request.method == 'POST':
        security_form = SecurityCodeForm(request.POST)
        if security_form.is_valid():
            code_de_securite = security_form.cleaned_data['code_de_securite']
            if profil.code_de_securite == code_de_securite:
                form = ResetPasswordForm(request.POST)
                if form.is_valid():
                    new_password = form.cleaned_data['new_password']
                    utilisateur.set_password(new_password)
                    utilisateur.save()
                    messages.success(request, f"Le mot de passe de {utilisateur.username} a été réinitialisé avec succès.")
                    return redirect('liste_enseignants')
            else:
                messages.error(request, "Le code de sécurité est incorrect.")
                form = ResetPasswordForm()
        else:
            form = ResetPasswordForm()
    else:
        form = ResetPasswordForm()
        security_form = SecurityCodeForm()

    context = {
        'form': form,
        'security_form': security_form,
        'utilisateur': utilisateur
    }
    return render(request, 'utilisateurs/reset_password.html', context)


@role_required(allowed_roles=['Admin_', 'SG'])   
@login_required(login_url='login')
def supprimer_enseignant(request, user_id):
    utilisateur = get_object_or_404(User, id=user_id)
    profil = get_object_or_404(ProfilUtilisateur, utilisateur=utilisateur)

    if request.method == 'POST':
        code_de_securite = request.POST.get('code_de_securite')
        if code_de_securite == request.user.profilutilisateur.code_de_securite:
            profil.actif = False
            profil.save()
            messages.success(request, f"L'enseignant {utilisateur.username} a été désactivé avec succès.")
            return redirect('liste_enseignants')
        else:
            messages.error(request, 'Code de sécurité incorrect.')

    return render(request, 'utilisateurs/supprimer_enseignant.html', {'enseignant': utilisateur})

@role_required(allowed_roles=['Admin_', 'AP', 'SG'])
@login_required(login_url='login')
def notifier(request, user_id):
    receiver = get_object_or_404(User, id=user_id)

    if request.method == 'POST':
        message = request.POST.get('message')
        Notification.objects.create(sender=request.user, receiver=receiver, message=message)
        messages.success(request, f"Notification envoyée à {receiver.username}.")
        return redirect('liste_enseignants')
    
    return render(request, 'utilisateurs/notifier.html', {'receiver': receiver})

@login_required(login_url='login')
def notifications(request):
    notifications = Notification.objects.filter(receiver=request.user).order_by('-date_sent')
    unread_notifications = notifications.filter(is_read=False)
    # Marquer les notifications comme lues
    unread_notifications.update(is_read=True)
    context = {
        'notifications': notifications,
    }
    return render(request, 'utilisateurs/notifications.html', context)

@role_required(allowed_roles=['Admin_', 'SG'])
@login_required(login_url='login')
def demander_code_securite(request, pk):
    enseignant = ProfilUtilisateur.objects.get(id=pk)
    if request.method == 'POST':
        form = SecurityCodeForm(request.POST)
        if form.is_valid():
            if form.cleaned_data['code_de_securite'] == enseignant.code_de_securite:
                return redirect('reinitialiser_mot_de_passe', pk=pk)
            else:
                messages.error(request, 'Code de sécurité incorrect.')
    else:
        form = SecurityCodeForm()
    return render(request, 'utilisateurs/demander_code_securite.html', {'form': form})

@role_required(allowed_roles=['Admin_', 'SG'])
@login_required(login_url='login')
def reinitialiser_mot_de_passe(request, pk):
    utilisateur = get_object_or_404(User, id=pk)
    profil = get_object_or_404(ProfilUtilisateur, utilisateur=utilisateur)

    # Vérifier si l'utilisateur a un code de sécurité défini
    if not profil.code_de_securite:
        messages.error(request, f"L'utilisateur {profil.nom} n'a pas de code de sécurité défini.")
        return redirect('liste_enseignants')

    if request.method == 'POST':
        security_code = request.POST.get('code_de_securite')
        new_password = request.POST.get('new_password')
        confirm_password = request.POST.get('confirm_password')

        if security_code == profil.code_de_securite:
            if new_password == confirm_password:
                utilisateur.set_password(new_password)
                utilisateur.save()
                messages.success(request, f"Le mot de passe de {profil.nom} a été réinitialisé avec succès.")
                return redirect('liste_enseignants')
            else:
                messages.error(request, 'Les mots de passe ne correspondent pas.')
        else:
            messages.error(request, 'Code de sécurité incorrect.')

    context = {
        'utilisateur': utilisateur
    }
    return render(request, 'utilisateurs/reinitialiser_mot_de_passe.html', context)



@login_required(login_url='login')
def sent_notifications(request):
    sent_notifications = Notification.objects.filter(sender=request.user).order_by('-date_sent')
    context = {
        'sent_notifications': sent_notifications,
    }
    return render(request, 'utilisateurs/sent_notifications.html', context)



@login_required(login_url='login')
def confirmer_suppression(request, user_id):
    utilisateur = get_object_or_404(User, id=user_id)
    profil = get_object_or_404(ProfilUtilisateur, utilisateur=utilisateur)

    if request.method == 'POST':
        profil.actif = False
        profil.save()

        # Générer un mot de passe aléatoire
        random_password = get_random_string(length=12)

        # Réinitialiser le mot de passe de l'utilisateur
        utilisateur.set_password(random_password)
        utilisateur.save()

        messages.success(request, f"L'enseignant {profil.nom} a été désactivé avec succès. Un mot de passe aléatoire a été attribué pour empêcher toute connexion future.")
        return redirect('liste_enseignants')
    
    context = {
        'enseignant': profil
    }
    return render(request, 'utilisateurs/confirmer_suppression.html', context)

@login_required(login_url='login')
@role_required(allowed_roles=['Admin_', 'SG'])
def liste_departements(request):
    if request.user.profilutilisateur.role == 'Admin_':
        departements = Departement.objects.all().order_by('nom')
    else:
        departements = Departement.objects.filter(utilisateur_sg=request.user.profilutilisateur).order_by('nom')
    
    query = request.GET.get('q')
    if query:
        departements = departements.filter(
            Q(nom__icontains=query) |
            Q(description__icontains=query) |
            Q(chef_departement__nom__icontains=query)
        )

    paginator = Paginator(departements, 10)  # Paginer la liste des départements
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'departements/liste_departements.html', {'page_obj': page_obj, 'query': query})



@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def ajouter_departement(request):
    if request.method == 'POST':
        form = DepartementForm(request.POST)
        if form.is_valid():
            print("Formulaire valide")
            departement = form.save(commit=False)
            departement.save()

            # Associer le SG sélectionné au département
            utilisateur_sg = form.cleaned_data['utilisateur_sg']
            print(f"Utilisateur SG: {utilisateur_sg}")
            EnseignantDepartement.objects.create(
                enseignant=utilisateur_sg,
                departement=departement,
                is_chef_departement=False
            )
            messages.success(request, "Département ajouté avec succès.")
            return redirect('liste_departements')
        else:
            # Message d'erreur si le formulaire n'est pas valide
            messages.error(request, "Veuillez remplir tous les champs svp.")
            #print(f"Formulaire non valide: {form.errors}")  # Pour le débogage
    else:
        form = DepartementForm()
    
    return render(request, 'departements/ajouter_departement.html', {'form': form})



@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def modifier_departement(request, departement_id):
    departement = get_object_or_404(Departement, id=departement_id)
    if request.method == 'POST':
        form = DepartementForm(request.POST, instance=departement)
        if form.is_valid():
            form.save()
            messages.success(request, "Département modifié avec succès.")
            return redirect('liste_departements')
    else:
        form = DepartementForm(instance=departement)
    return render(request, 'departements/modifier_departement.html', {'form': form})

@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def supprimer_departement(request, departement_id):
    return supprimer_objet_securise(
        request, 
        model=Departement, 
        pk=departement_id, 
        redirect_url='liste_departements'
    )




@role_required(allowed_roles=['Admin_', 'SG'])    
@login_required(login_url='login')
def menu_gestion_departements(request):
    return render(request, 'departements/menu_gestion_departements.html')

@login_required
def confirmer_suppression_departement(request, departement_id):
    departement = get_object_or_404(Departement, id=departement_id)
    return render(request, 'departements/confirmer_suppression_departement.html', {'departement': departement})

@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def assigner_enseignant(request, enseignant_id=None):
    if request.method == 'POST':
        form = AssignationForm(request.POST)
        if form.is_valid():
            enseignant = form.cleaned_data['enseignant']
            departements = form.cleaned_data['departements']
            is_chef_departement = form.cleaned_data['is_chef_departement']
            
            # Enlever tous les départements actuels
            EnseignantDepartement.objects.filter(enseignant=enseignant).delete()

            # Ajouter les nouveaux départements
            for departement in departements:
                EnseignantDepartement.objects.create(enseignant=enseignant, departement=departement, is_chef_departement=is_chef_departement)
            
            messages.success(request, "Enseignant assigné aux départements avec succès.")
            return redirect('liste_enseignants_par_departement')
    else:
        if enseignant_id:
            enseignant = get_object_or_404(ProfilUtilisateur, id=enseignant_id)
            form = AssignationForm(initial={'enseignant': enseignant})
        else:
            form = AssignationForm()
    return render(request, 'utilisateurs/assigner_enseignant.html', {'form': form})



@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def liste_enseignants_par_departement(request):
    query = request.GET.get('q')
    departements = Departement.objects.all().order_by('nom')

    if query:
        # Filtrer les départements en fonction des enseignants dont le nom contient la requête
        departements = departements.filter(
            Q(nom__icontains=query) |
            Q(description__icontains=query) |
            Q(enseignants__nom__icontains=query) |
            Q(enseignants__matricule__icontains=query) |
            Q(enseignants__role__icontains=query)
        ).distinct()

    paginator = Paginator(departements, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    # Récupérer les paramètres de l'établissement
    parametres = ParametresEtablissement.objects.first()

    context = {
        'departements': departements,
        'page_obj': page_obj,
        'query': query,
        'parametres': parametres,  # Ajouter les paramètres de l'établissement au contexte
    }
    return render(request, 'utilisateurs/liste_enseignants_par_departement.html', context)

@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def imprimer_liste_enseignants_par_departement(request):
    departements = Departement.objects.all().order_by('nom')
    parametres = ParametresEtablissement.objects.first()

    context = {
        'departements': departements,
        'parametres': parametres,
    }

    template_path = 'utilisateurs/liste_enseignants_par_departement_pdf.html'
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="Liste_Enseignants_Departements.pdf"'
    template = get_template(template_path)
    html = template.render(context)

    pisa_status = pisa.CreatePDF(html, dest=response)
    if pisa_status.err:
        return HttpResponse('Une erreur s\'est produite lors de la génération du PDF', status=400)
    return response


@role_required(allowed_roles=['Admin_', 'SG'])
@login_required
def supprimer_departement_enseignant(request, enseignant_id, departement_id):
    enseignant = get_object_or_404(ProfilUtilisateur, id=enseignant_id)
    departement = get_object_or_404(Departement, id=departement_id)

    if request.method == 'POST':
        # Suppression de l'association entre l'enseignant et le département
        EnseignantDepartement.objects.filter(enseignant=enseignant, departement=departement).delete()
        messages.success(request, f"L'enseignant {enseignant.nom} a été retiré du département {departement.nom}.")
        return redirect('liste_enseignants_par_departement')
    
    context = {
        'enseignant': enseignant,
        'departement': departement
    }
    return render(request, 'utilisateurs/confirmer_suppression.html', context)


@login_required
def supprimer_objet_securise(request, model, pk, redirect_url):
    """
    Vue générique pour supprimer un objet avec vérification du code de sécurité.

    :param request: Requête HTTP
    :param model: Le modèle de l'objet à supprimer (ex: Eleve, Classe, etc.)
    :param pk: ID de l'objet à supprimer
    :param redirect_url: URL vers laquelle rediriger après la suppression réussie
    """
    obj = get_object_or_404(model, pk=pk)
    profil = request.user.profilutilisateur

    if request.method == 'POST':
        form = SecurityCodeForm(request.POST)
        if form.is_valid():
            code_de_securite = form.cleaned_data['code_de_securite']
            if profil.code_de_securite == code_de_securite:
                obj.delete()
                messages.success(request, f"{model.__name__} supprimé avec succès.")
                return redirect(redirect_url)
            else:
                messages.error(request, "Code de sécurité incorrect.")
        else:
            messages.error(request, "Formulaire invalide.")
    else:
        form = SecurityCodeForm()

    context = {
        'obj': obj,
        'form': form,
        'title': f"Supprimer {model.__name__}",
    }

    return render(request, 'suppression/securisee.html', context)

def assigner_classe(request, enseignant_id):
    enseignant = get_object_or_404(ProfilUtilisateur, id=enseignant_id)

    if request.method == 'POST':
        form = AssignerClasseForm(request.POST, instance=enseignant)
        if form.is_valid():
            # Si un enseignant est déjà responsable d'une classe, on libère cette classe
            if enseignant.responsable_classe:
                ancienne_classe = enseignant.responsable_classe
                ancienne_classe.responsable = None
                ancienne_classe.save()

            # Assignation de la nouvelle classe
            nouvelle_classe = form.cleaned_data['responsable_classe']
            enseignant.responsable_classe = nouvelle_classe
            enseignant.save()

            # Mettre à jour la classe choisie (si ce n'est pas "Aucune classe")
            if nouvelle_classe:
                nouvelle_classe.responsable = enseignant
                nouvelle_classe.save()

            messages.success(request, f"Classe {nouvelle_classe.nom if nouvelle_classe else 'Aucune classe'} assignée à {enseignant.nom}.")
            return redirect('liste_enseignants')
    else:
        form = AssignerClasseForm(instance=enseignant)

    return render(request, 'utilisateurs/assigner_classe.html', {'form': form, 'enseignant': enseignant})