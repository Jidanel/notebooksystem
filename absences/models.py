# absences/models.py
from django.db import models
from eleves.models import Eleve
from classes.models import Classe
from utilisateurs.models import ProfilUtilisateur

class Absence(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    sequence = models.CharField(max_length=10)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(ProfilUtilisateur, on_delete=models.CASCADE)
    absences = models.IntegerField(default=0)
    justification = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        # Convertir en entier si nécessaire
        self.absences = int(self.absences)
        self.justification = int(self.justification)
        
        self.total = self.absences - self.justification
        super(Absence, self).save(*args, **kwargs)


    def __str__(self):
        return f"{self.eleve.nom} - {self.classe.nom} - {self.sequence}"
