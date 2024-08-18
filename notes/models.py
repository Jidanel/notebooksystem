from django.db import models
from utilisateurs.models import ProfilUtilisateur
from eleves.models import Eleve
from classes.models import Classe
from cours.models import Matiere
from django.core.exceptions import ValidationError

class Note(models.Model):
    SEQUENCE_CHOICES = [
        ('Seq1', 'Séquence 1'),
        ('Seq2', 'Séquence 2'),
        ('Seq3', 'Séquence 3'),
        ('Seq4', 'Séquence 4'),
        ('Seq5', 'Séquence 5'),
    ]

    APPRECIATION_CHOICES = [
        ('Non acquis', 'NON ACQUIS'),
        ('En cours', 'EN COURS'),
        ('Acquis', 'ACQUIS'),
    ]

    eleve = models.ForeignKey(Eleve, related_name='notes', on_delete=models.CASCADE)
    enseignant = models.ForeignKey(ProfilUtilisateur, related_name='notes', on_delete=models.CASCADE)
    classe = models.ForeignKey(Classe, related_name='notes', on_delete=models.CASCADE)
    matiere = models.ForeignKey(Matiere, related_name='notes', on_delete=models.CASCADE)
    sequence = models.CharField(max_length=10, choices=SEQUENCE_CHOICES)
    note = models.FloatField()
    appreciation = models.CharField(max_length=20, choices=APPRECIATION_CHOICES, blank=True)
    rang = models.IntegerField(null=True, blank=True)
    completed = models.BooleanField(default=False)  # Champ pour indiquer si les notes sont complètes
    

    class Meta:
        unique_together = ('eleve', 'matiere', 'sequence')

    def clean(self):
        if self.note < 0 or self.note > 20:
            raise ValidationError('La note doit être entre 0 et 20.')

    def save(self, *args, **kwargs):
        self.set_appreciation()
        super().save(*args, **kwargs)

    def set_appreciation(self):
        try:
            note_value = float(self.note)  # Convertir la note en float
        except ValueError:
            # Si la conversion échoue, définissez une appréciation par défaut ou laissez l'appréciation vide
            self.appreciation = ''
            return

        if 0 <= note_value <= 9.99:
            self.appreciation = 'Non acquis'
        elif 10 <= note_value <= 12.99:
            self.appreciation = 'En cours'
        elif note_value >= 13:
            self.appreciation = 'Acquis'

    def __str__(self):
        return f"Note de {self.eleve} en {self.matiere} ({self.sequence}) - {self.note} ({self.appreciation})"
