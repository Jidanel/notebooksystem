# absences/models.py
from django.db import models
from eleves.models import Eleve
from classes.models import Classe
from utilisateurs.models import ProfilUtilisateur
from django.core.exceptions import ValidationError

class Absence(models.Model):
    eleve = models.ForeignKey(Eleve, on_delete=models.CASCADE)
    sequence = models.CharField(max_length=10)
    classe = models.ForeignKey(Classe, on_delete=models.CASCADE)
    enseignant = models.ForeignKey(ProfilUtilisateur, on_delete=models.CASCADE)
    absences = models.IntegerField(default=0)
    justification = models.IntegerField(default=0)
    total = models.IntegerField(default=0)

    class Meta:
        indexes = [
            models.Index(fields=['eleve']),  # Index sur le champ 'eleve'
            models.Index(fields=['classe']),  # Index sur le champ 'classe'
            models.Index(fields=['enseignant']),  # Index sur le champ 'enseignant'
            models.Index(fields=['sequence']),  # Index sur le champ 'sequence'
        ]
    
    def clean(self):
        if self.justification > self.absences:
            raise ValidationError("Les heures d'absences justifiées sont superieures aux heures non justifiées.")
        
    def save(self, *args, **kwargs):
        self.absences = int(self.absences)
        self.justification = int(self.justification)
        self.total = self.absences - self.justification
        super(Absence, self).save(*args, **kwargs)

    def __str__(self):
        return f"{self.eleve.nom} - {self.classe.nom} - {self.sequence}"
