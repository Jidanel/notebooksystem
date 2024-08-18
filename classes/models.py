from django.db import models
from django.contrib.auth.models import User
from utilisateurs.models import *

class Classe(models.Model):
    nom = models.CharField(max_length=100)
    code = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.nom
