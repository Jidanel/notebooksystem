# cours/urls.py
from django.urls import path
from . import views

urlpatterns = [
    path('matieres/', views.liste_matieres, name='liste_matieres'),
    path('matieres/ajouter/', views.ajouter_matiere, name='ajouter_matiere'),
    path('matieres/modifier/<int:matiere_id>/', views.modifier_matiere, name='modifier_matiere'),
    path('matieres/supprimer/<int:matiere_id>/', views.confirmer_suppression_matiere, name='confirmer_suppression_matiere'),
    path('matieres/filtrer_enseignants/', views.filtrer_enseignants_par_departement, name='filtrer_enseignants_par_departement'),

]
