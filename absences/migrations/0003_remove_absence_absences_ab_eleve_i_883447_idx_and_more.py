# Generated by Django 5.0.7 on 2024-09-01 15:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('absences', '0002_alter_absence_sequence_and_more'),
        ('classes', '0002_classe_classes_cla_nom_265e0a_idx_and_more'),
        ('eleves', '0002_eleve_eleves_elev_nom_0d618a_idx_and_more'),
        ('utilisateurs', '0001_initial'),
    ]

    operations = [
        migrations.RemoveIndex(
            model_name='absence',
            name='absences_ab_eleve_i_883447_idx',
        ),
        migrations.RemoveIndex(
            model_name='absence',
            name='absences_ab_classe__a1f8de_idx',
        ),
        migrations.AlterField(
            model_name='absence',
            name='sequence',
            field=models.CharField(max_length=10),
        ),
        migrations.AddIndex(
            model_name='absence',
            index=models.Index(fields=['eleve'], name='absences_ab_eleve_i_33c3a2_idx'),
        ),
        migrations.AddIndex(
            model_name='absence',
            index=models.Index(fields=['classe'], name='absences_ab_classe__bac549_idx'),
        ),
        migrations.AddIndex(
            model_name='absence',
            index=models.Index(fields=['enseignant'], name='absences_ab_enseign_9696fe_idx'),
        ),
        migrations.AddIndex(
            model_name='absence',
            index=models.Index(fields=['sequence'], name='absences_ab_sequenc_0b45a2_idx'),
        ),
    ]
