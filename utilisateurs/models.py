from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from classes.models import *

class Departement(models.Model):
    nom = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    chef_departement = models.ForeignKey('ProfilUtilisateur', related_name='chef_departement', on_delete=models.SET_NULL, null=True, blank=True)
    utilisateur_sg = models.ForeignKey('ProfilUtilisateur', related_name='departements', on_delete=models.SET_NULL, null=True, blank=True)  # Ajoutez ce champ
    def __str__(self):
        return self.nom

class ProfilUtilisateur(models.Model):
    utilisateur = models.OneToOneField(User, on_delete=models.CASCADE)
    nom = models.CharField(max_length=100, blank=True, null=True)
    matricule = models.CharField(max_length=50, unique=True, blank=True, null=True)
    code_de_securite = models.CharField(max_length=10, blank=True, null=True)
    sexe = models.CharField(max_length=10, choices=[('M', 'Masculin'), ('F', 'Féminin')], blank=True, null=True)  # Ajout du champ sexe
    role = models.CharField(max_length=50, default='Enseignant', choices=[
        ('Enseignant', 'Enseignant'),
        ('AP', 'Animateur Pedagogique'),
        ('SG', 'Surveillant General'),
        ('Admin_', 'Admininistrateur'),
    ], blank=True, null=True)
    profile_img = models.ImageField(default='images/default.jpg', upload_to='images', null=True, blank=True)
    actif = models.BooleanField(default=True)
    responsable_classe = models.OneToOneField(Classe, on_delete=models.SET_NULL, null=True, blank=True, related_name='responsable')  # Le champ que vous avez demandé


    def __str__(self):
        return f"{self.nom} - {self.utilisateur.username}"

class EnseignantDepartement(models.Model):
    enseignant = models.ForeignKey(ProfilUtilisateur, on_delete=models.CASCADE)
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE)
    is_chef_departement = models.BooleanField(default=False)

    class Meta:
        unique_together = ('enseignant', 'departement')

    def __str__(self):
        return f"{self.enseignant.nom} - {self.departement.nom}"

@receiver(post_save, sender=Departement)
def add_chef_departement(sender, instance, created, **kwargs):
    if created and instance.chef_departement:
        EnseignantDepartement.objects.create(
            enseignant=instance.chef_departement,
            departement=instance,
            is_chef_departement=True
        )

class Notification(models.Model):
    sender = models.ForeignKey(User, related_name='sent_notifications', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_notifications', on_delete=models.CASCADE)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    date_sent = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Notification from {self.sender} to {self.receiver}'
