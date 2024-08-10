from django.db import models
from classes.models import Classe

class Eleve(models.Model):
    photo = models.ImageField(upload_to='eleves/photos', null=True, blank=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=10, choices=[('Masculin', 'Masculin'), ('Féminin', 'Féminin')])
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100)
    adresse = models.TextField(null=True, blank=True)
    classe_actuelle = models.ForeignKey(Classe, related_name='eleves', on_delete=models.SET_NULL, null=True)
    matricule = models.CharField(max_length=50, unique=True)
    statut = models.CharField(max_length=10, choices=[('Nouveau', 'Nouveau'), ('Redoublant', 'Redoublant')])
    contact_parent = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.nom} {self.prenom}"
