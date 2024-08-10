from django.urls import path
from .views import *

urlpatterns = [
    path('eleves/', liste_eleves, name='liste_eleves'),
    path('eleves/ajouter/', ajouter_eleve, name='ajouter_eleve'),
    path('eleves/modifier/<int:eleve_id>/', modifier_eleve, name='modifier_eleve'),
    path('eleves/confirmer_suppression/<int:eleve_id>/', confirmer_suppression_eleve, name='confirmer_suppression_eleve'),
    path('eleves/importer/', importer_eleves, name='importer_eleves'),
    path('eleves/contacter/<int:eleve_id>/', contacter_parents, name='contacter_parents'),
    path('resolve_duplicates/', resolve_duplicates, name='resolve_duplicates'),
    path('liste_par_classe/', liste_eleves_par_classe, name='liste_eleves_par_classe'),
    path('imprimer_liste/<int:classe_id>/', imprimer_liste_eleves, name='imprimer_liste_eleves'),
    path('eleves/resolve_import_errors/', resolve_import_errors, name='resolve_import_errors'),
]
 
