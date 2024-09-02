# classes/models.py
from django.db import models
from utilisateurs.models import *

class Classe(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)

    class Meta:
        indexes = [
            models.Index(fields=['nom']),  # Index sur le champ 'nom'
            models.Index(fields=['code']),  # Index sur le champ 'code'
        ]

    def __str__(self):
        return self.nom
