# Generated by Django 5.0.7 on 2024-08-01 11:21

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('utilisateurs', '0015_remove_profilutilisateur_inactif_and_more'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='profilutilisateur',
            name='is_chef_departement',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='profilutilisateur',
            name='role',
            field=models.CharField(blank=True, choices=[('Enseignant', 'Enseignant'), ('AP', 'Animateur Pedagogique'), ('SG', 'Surveillant General'), ('Admin_', 'Admininistrateur')], default='Enseignant', max_length=50, null=True),
        ),
        migrations.CreateModel(
            name='Departement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('chef_departement', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='chef_departement', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='profilutilisateur',
            name='departement',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='enseignants', to='utilisateurs.departement'),
        ),
        migrations.CreateModel(
            name='Matiere',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom', models.CharField(max_length=100)),
                ('description', models.TextField(blank=True, null=True)),
                ('coefficient', models.DecimalField(decimal_places=2, max_digits=5)),
                ('departement', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='matieres', to='utilisateurs.departement')),
            ],
        ),
    ]
