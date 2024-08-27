from django.urls import path
from . import views

urlpatterns = [
    path('gestion-trimestres/', views.menu_gestion_trimestres, name='menu_gestion_trimestres'),
    path('gestion-trimestre-1/', views.menu_gestion_trimestre_1, name='menu_gestion_trimestre_1'),
    path('bulletins_et_stats/', views.bulletins_et_stats, name='bulletins_et_stats'),
    path('selection_classe_matiere/<str:sequence>/', views.selection_classe_matiere, name='selection_classe_matiere'),
    path('saisie-notes/<str:sequence>/<int:classe_id>/<int:matiere_id>/', views.saisie_notes, name='saisie_notes'),
    path('notes-completes/', views.liste_notes_completes, name='liste_notes_completes'),

    # Alias pour chaque séquence
    path('selection_classe_matiere_seq2/', views.selection_classe_matiere_seq2, name='selection_classe_matiere_seq2'),
    path('saisie-notes_seq2/<int:classe_id>/<int:matiere_id>/', views.saisie_notes_seq2, name='saisie_notes_seq2'),

    # URL pour afficher les statistiques d'une matière
    path('statistiques/<str:sequence>/<int:classe_id>/<int:matiere_id>/', views.afficher_statistiques_matiere, name='afficher_statistiques_matiere'),

    #url pour afficher les statistiques des sequences
    path('statistiques/sequence/<int:classe_id>/<str:sequence>/', views.afficher_statistiques_sequence, name='afficher_statistiques_sequence'),

    # URL pour afficher les statistiques du trimestre 1
    path('statistiques/trimestre/<int:classe_id>/', views.afficher_statistiques_trimestre, name='afficher_statistiques_trimestre'),
    path('bulletins/<int:classe_id>/', views.afficher_bulletins_trimestriels, name='afficher_bulletins_trimestriels'),
    # Route pour afficher les bulletins de la Séquence 1
    path('notes/bulletins_seq1/<int:classe_id>/', views.afficher_bulletins_sequence1, name='bulletins_seq1'),
    
    # Route pour afficher les bulletins de la Séquence 2
    path('notes/bulletins_seq2/<int:classe_id>/', views.afficher_bulletins_sequence2, name='bulletins_seq2'),
    path('liste_classes_par_sequence', views.liste_classes_par_sequence, name='liste_classes_par_sequence'),
    path('bordereau_par_sequence', views.bordereau_par_sequence, name='bordereau_par_sequence'),
    path('matieres_incompletes/<int:classe_id>/<str:sequence>/', views.liste_matieres_incompletes_par_classe, name='liste_matieres_incompletes_par_classe'),
    path('imprimer-bordereau/<int:classe_id>/<str:sequence>/', views.imprimer_bordereau_notes, name='imprimer_bordereau_notes'),

]
