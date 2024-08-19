from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import *

router = DefaultRouter()
router.register(r'eleves', EleveViewSet)
router.register(r'classes', ClasseViewSet)
router.register(r'notes', NoteViewSet)
router.register(r'absences', AbsenceViewSet)
router.register(r'profils', ProfilUtilisateurViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('meilleures_matieres_par_classe/', meilleures_matieres_par_classe, name='meilleures_matieres_par_classe'),  # Ajouter cette ligne
    path('meilleure_classe/', meilleure_classe, name='meilleure_classe'),  # Ajouter cette ligne
    path('meilleures_classes_par_sequence/',  meilleures_classes_par_sequence, name=' meilleures_classes_par_sequence'),  # Ajouter cette ligne
    path('matieres_avec_moins_de_reussite_par_classe/',matieres_avec_moins_de_reussite_par_trimestre, name='matieres_avec_moins_de_reussite_par_classe'),  # Ajouter cette ligne
    path('sequences/', get_sequences, name='get_sequences'), 
]
