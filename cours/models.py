# cours/models.py
from django.db import models
from utilisateurs.models import Departement, ProfilUtilisateur
from classes.models import Classe

class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    coefficient = models.IntegerField()
    departement = models.ForeignKey(Departement, related_name='cours_matieres', on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, related_name='matieres', on_delete=models.CASCADE)
    enseignant = models.ForeignKey(ProfilUtilisateur, related_name='matieres', on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return self.nom
