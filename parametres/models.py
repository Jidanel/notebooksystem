from django.db import models

class ParametresEtablissement(models.Model):
    nom_etablissement_fr = models.CharField(max_length=255, verbose_name="Nom de l'établissement")
    nom_etablissement_en = models.CharField(max_length=255, verbose_name="Name of the School")
    bp_fr = models.CharField(max_length=255, verbose_name="Boîte Postale")
    bp_en = models.CharField(max_length=255, verbose_name="PO Box")
    telephone_fr = models.CharField(max_length=255, verbose_name="Téléphone")
    telephone_en = models.CharField(max_length=255, verbose_name="Phone")
    ville_fr = models.CharField(max_length=255, verbose_name="Ville")
    ville_en = models.CharField(max_length=255, verbose_name="Town")
    annee_scolaire = models.CharField(max_length=9, verbose_name="Année Scolaire")
    logo = models.URLField(max_length=1024, null=True, blank=True, verbose_name="URL du Logo")

    def __str__(self):
        return self.nom_etablissement_fr
