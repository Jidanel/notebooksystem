from django.urls import path
from . import views

urlpatterns = [
    path('gestion-trimestres/', views.menu_gestion_trimestres, name='menu_gestion_trimestres'),
    path('gestion-trimestre-1/', views.menu_gestion_trimestre_1, name='menu_gestion_trimestre_1'),
    path('selection_classe_matiere/<str:sequence>/', views.selection_classe_matiere, name='selection_classe_matiere'),
    path('saisie-notes/<str:sequence>/<int:classe_id>/<int:matiere_id>/', views.saisie_notes, name='saisie_notes'),
    path('notes-completes/', views.liste_notes_completes, name='liste_notes_completes'),

    # Alias pour chaque séquence
    path('selection_classe_matiere_seq2/', views.selection_classe_matiere_seq2, name='selection_classe_matiere_seq2'),
    path('saisie-notes_seq2/<int:classe_id>/<int:matiere_id>/', views.saisie_notes_seq2, name='saisie_notes_seq2'),
]
