from django.db import models
from utilisateurs.models import Departement, ProfilUtilisateur
from classes.models import Classe
from notes.models import *

class Matiere(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    coefficient = models.IntegerField()
    departement = models.ForeignKey(Departement, related_name='cours_matieres', on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, related_name='matieres', on_delete=models.CASCADE)
    enseignant = models.ForeignKey(ProfilUtilisateur, related_name='matieres', on_delete=models.SET_NULL, null=True)
    groupe = models.CharField(max_length=50, null=True, blank=True)

    def __str__(self):
        return self.nom


class MatiereSequenceStatus(models.Model):
    matiere = models.ForeignKey(Matiere, related_name='sequence_status', on_delete=models.CASCADE)
    sequence = models.CharField(max_length=10, choices=[('Seq1', 'Séquence 1'), ('Seq2', 'Séquence 2'), ('Seq3', 'Séquence 3'), ('Seq4', 'Séquence 4'), ('Seq5', 'Séquence 5')])
    note_complete = models.BooleanField(default=False)

    class Meta:
        unique_together = ('matiere', 'sequence')

    def __str__(self):
        return f"{self.matiere.nom} - {self.sequence} : {'Complet' if self.note_complete else 'Incomplet'}"
