# Generated by Django 5.0.7 on 2024-08-25 11:27

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classes', '0001_initial'),
        ('eleves', '0001_initial'),
        ('utilisateurs', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Absence',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sequence', models.CharField(max_length=10)),
                ('absences', models.IntegerField(default=0)),
                ('justification', models.IntegerField(default=0)),
                ('total', models.IntegerField(default=0)),
                ('classe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.classe')),
                ('eleve', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='eleves.eleve')),
                ('enseignant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='utilisateurs.profilutilisateur')),
            ],
        ),
    ]
