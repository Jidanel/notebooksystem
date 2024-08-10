# licences/models.py
from django.db import models
from django.utils import timezone
from datetime import timedelta

class Licence(models.Model):
    code = models.CharField(max_length=20, unique=True)
    date_debut = models.DateTimeField(auto_now_add=True)
    duree_jours = models.IntegerField(default=365)  # Durée en jours
    date_expiration = models.DateTimeField(default=timezone.now() + timedelta(days=365))  # Définir une valeur par défaut pour la date d'expiration
    active = models.BooleanField(default=True)

    def save(self, *args, **kwargs):
        if not self.date_expiration:
            self.date_expiration = timezone.now() + timedelta(days=self.duree_jours)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.code
