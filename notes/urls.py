from django.urls import path
from . import views

urlpatterns = [
    path('gestion-trimestres/', views.menu_gestion_trimestres, name='menu_gestion_trimestres'),
    path('gestion_stats_departements/', views.gestion_stats_departements, name='gestion_stats_departements'),
    path('gestion-trimestre-1/', views.menu_gestion_trimestre_1, name='menu_gestion_trimestre_1'),
    path('gestion-trimestre-2/', views.menu_gestion_trimestre_2, name='menu_gestion_trimestre_2'),
    path('gestion-trimestre-3/', views.menu_gestion_trimestre_3, name='menu_gestion_trimestre_3'),
    path('bulletins_et_stats/', views.bulletins_et_stats, name='bulletins_et_stats'),
    path('selection_classe_matiere/<str:sequence>/', views.selection_classe_matiere, name='selection_classe_matiere'),
    path('saisie-notes/<str:sequence>/<int:classe_id>/<int:matiere_id>/', views.saisie_notes, name='saisie_notes'),
    path('notes-completes/', views.liste_notes_completes, name='liste_notes_completes'),

    # Alias pour chaque séquence
    path('selection_classe_matiere_seq2/', views.selection_classe_matiere_seq2, name='selection_classe_matiere_seq2'),
    path('saisie-notes_seq2/<int:classe_id>/<int:matiere_id>/', views.saisie_notes_seq2, name='saisie_notes_seq2'),

    # Alias pour les autres séquences
    path('selection_classe_matiere_seq3/', views.selection_classe_matiere_seq3, name='selection_classe_matiere_seq3'),
    path('selection_classe_matiere_seq4/', views.selection_classe_matiere_seq4, name='selection_classe_matiere_seq4'),
    path('selection_classe_matiere_seq5/', views.selection_classe_matiere_seq5, name='selection_classe_matiere_seq5'),

    path('saisie-notes_seq3/<int:classe_id>/<int:matiere_id>/', views.saisie_notes_seq3, name='saisie_notes_seq3'),
    path('saisie-notes_seq4/<int:classe_id>/<int:matiere_id>/', views.saisie_notes_seq4, name='saisie_notes_seq4'),
    path('saisie-notes_seq5/<int:classe_id>/<int:matiere_id>/', views.saisie_notes_seq5, name='saisie_notes_seq5'),

    # URL pour afficher les statistiques d'une matière
    path('statistiques/<str:sequence>/<int:classe_id>/<int:matiere_id>/', views.afficher_statistiques_matiere, name='afficher_statistiques_matiere'),

    # URL pour afficher les statistiques des séquences
    path('statistiques/sequence/<int:classe_id>/<str:sequence>/', views.afficher_statistiques_sequence, name='afficher_statistiques_sequence'),

    # URL pour afficher les statistiques des trimestres
    path('statistiques/trimestre1/<int:classe_id>/', views.afficher_statistiques_trimestre, name='afficher_statistiques_trimestre'),
    path('statistiques/trimestre2/<int:classe_id>/', views.afficher_statistiques_trimestre2, name='afficher_statistiques_trimestre2'),
    path('statistiques/trimestre3/<int:classe_id>/', views.afficher_statistiques_trimestre3, name='afficher_statistiques_trimestre3'),

    # URL pour afficher les statistiques annuelles
    path('statistiques/annuelles/<int:classe_id>/', views.afficher_statistiques_annuelles, name='afficher_statistiques_annuelles'),

    # URL pour afficher les bulletins trimestriels
    path('bulletins/trimestre1/<int:classe_id>/', views.afficher_bulletins_trimestriels, name='afficher_bulletins_trimestriels'),
    path('bulletins/trimestre2/<int:classe_id>/', views.afficher_bulletins_trimestre2, name='afficher_bulletins_trimestriels2'),
    path('bulletins/trimestre3/<int:classe_id>/', views.afficher_bulletins_trimestre3, name='afficher_bulletins_trimestriels3'),

    # URL pour afficher les bulletins des Séquences 1, 2, 3, 4, 5
    path('notes/bulletins_seq1/<int:classe_id>/', views.afficher_bulletins_sequence1, name='bulletins_seq1'),
    path('notes/bulletins_seq2/<int:classe_id>/', views.afficher_bulletins_sequence2, name='bulletins_seq2'),
    path('notes/bulletins_seq3/<int:classe_id>/', views.afficher_bulletins_sequence3, name='bulletins_seq3'),
    path('notes/bulletins_seq4/<int:classe_id>/', views.afficher_bulletins_sequence4, name='bulletins_seq4'),
    path('notes/bulletins_seq5/<int:classe_id>/', views.afficher_bulletins_sequence5, name='bulletins_seq5'),

    # URL pour afficher le bulletin annuel
    path('notes/bulletins_annuels/<int:classe_id>/', views.afficher_bulletins_annuels, name='bulletins_annuels'),

    # URL pour afficher les classes par séquence
    path('liste_classes_par_sequence/', views.liste_classes_par_sequence, name='liste_classes_par_sequence'),

    # URL pour le bordereau par séquence
    path('bordereau_par_sequence/', views.bordereau_par_sequence, name='bordereau_par_sequence'),

    # URL pour lister les matières incomplètes par classe
    path('matieres_incompletes/<int:classe_id>/<str:sequence>/', views.liste_matieres_incompletes_par_classe, name='liste_matieres_incompletes_par_classe'),

    # URL pour imprimer le bordereau des notes
    path('imprimer-bordereau/<int:classe_id>/<str:sequence>/', views.imprimer_bordereau_notes, name='imprimer_bordereau_notes'),

    # URL pour afficher les statistiques trimestrielles d'un département
    path('statistiques-trimestrielles-departement/<str:trimestre>/', views.statistiques_trimestrielles_departement, name='statistiques_trimestrielles_departement'),
    path('imprimer_bordereau_remplissage/<int:classe_id>/', views.imprimer_bordereau_remplissage, name='imprimer_bordereau_remplissage'),

]
