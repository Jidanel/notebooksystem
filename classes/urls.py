
from django.urls import path
from .views import *

urlpatterns = [
    path('classes/', liste_classes, name='liste_classes'),
    path('classes/ajouter/', ajouter_classe, name='ajouter_classe'),
    path('classes/modifier/<int:classe_id>/', modifier_classe, name='modifier_classe'),
    path('classes/confirmer_suppression/<int:classe_id>/', confirmer_suppression_classe, name='confirmer_suppression_classe'),
    path('classes/imprimer/<int:classe_id>/', imprimer_classe, name='imprimer_classe'),
    path('classes/details/<int:classe_id>/', details_classe, name='details_classe'),
    path('gestion-classes/', menu_gestion_classes, name='gestion_classes'),
]
