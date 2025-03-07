# Generated by Django 5.0.7 on 2024-09-01 23:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('classes', '0002_classe_classes_cla_nom_265e0a_idx_and_more'),
        ('cours', '0005_matiere_cours_matie_nom_6ae08c_idx_and_more'),
        ('eleves', '0002_eleve_eleves_elev_nom_0d618a_idx_and_more'),
        ('notes', '0001_initial'),
        ('utilisateurs', '0001_initial'),
    ]

    operations = [
        migrations.AddIndex(
            model_name='note',
            index=models.Index(fields=['eleve'], name='notes_note_eleve_i_7f021e_idx'),
        ),
        migrations.AddIndex(
            model_name='note',
            index=models.Index(fields=['enseignant'], name='notes_note_enseign_588bc3_idx'),
        ),
        migrations.AddIndex(
            model_name='note',
            index=models.Index(fields=['classe'], name='notes_note_classe__867a10_idx'),
        ),
        migrations.AddIndex(
            model_name='note',
            index=models.Index(fields=['matiere'], name='notes_note_matiere_640de6_idx'),
        ),
        migrations.AddIndex(
            model_name='note',
            index=models.Index(fields=['sequence'], name='notes_note_sequenc_19fd7f_idx'),
        ),
    ]
