from django.db import models
from classes.models import Classe

class Eleve(models.Model):
    photo = models.ImageField(upload_to='eleves/photos', null=True, blank=True)
    nom = models.CharField(max_length=100)
    prenom = models.CharField(max_length=100)
    sexe = models.CharField(max_length=10, choices=[('Masculin', 'Masculin'), ('Feminin', 'Feminin')])
    date_naissance = models.DateField()
    lieu_naissance = models.CharField(max_length=100)
    adresse = models.TextField(null=True, blank=True)
    classe_actuelle = models.ForeignKey(Classe, related_name='eleves', on_delete=models.SET_NULL, null=True)
    matricule = models.CharField(max_length=50, unique=True)
    statut = models.CharField(max_length=10, choices=[('Nouveau', 'Nouveau'), ('Redoublant', 'Redoublant')])
    contact_parent = models.CharField(max_length=15)

    class Meta:
        indexes = [
            models.Index(fields=['nom']),  # Index sur le champ 'nom'
            models.Index(fields=['matricule']),  # Index sur le champ 'matricule'
            models.Index(fields=['classe_actuelle']),  # Index sur le champ 'classe_actuelle'
            models.Index(fields=['statut']),  # Index sur le champ 'statut'
            models.Index(fields=['sexe']),  # Index sur le champ 'sexe'
        ]

    def __str__(self):
        return f"{self.nom} {self.prenom}"
