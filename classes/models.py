from django.db import models
from django.contrib.auth.models import User

class Classe(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)
    enseignant_titulaire = models.ForeignKey(User, related_name='classes', on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.nom
