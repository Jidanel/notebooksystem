from django.urls import path
from . import views

urlpatterns = [
    path('selection/', views.selection_classe_sequence, name='selection_classe_sequence'),
    path('saisie/<int:classe_id>/<str:sequence>/', views.saisie_absences, name='saisie_absences'),
    path('justifier/<str:sequence>/<int:classe_id>/', views.justifier_absences, name='justifier_absences'),
    path('imprimer/<str:sequence>/<int:classe_id>/', views.imprimer_absences, name='imprimer_absences'),
    path('liste/', views.liste_absences_completes, name='liste_absences_completes'),
   
]
