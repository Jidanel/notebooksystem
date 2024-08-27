# Generated by Django 5.0.7 on 2024-08-25 11:27

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ParametresEtablissement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nom_etablissement_fr', models.CharField(max_length=255, verbose_name="Nom de l'établissement")),
                ('nom_etablissement_en', models.CharField(max_length=255, verbose_name='Name of the School')),
                ('bp_fr', models.CharField(max_length=255, verbose_name='Boîte Postale')),
                ('bp_en', models.CharField(max_length=255, verbose_name='PO Box')),
                ('telephone_fr', models.CharField(max_length=255, verbose_name='Téléphone')),
                ('telephone_en', models.CharField(max_length=255, verbose_name='Phone')),
                ('ville_fr', models.CharField(max_length=255, verbose_name='Ville')),
                ('ville_en', models.CharField(max_length=255, verbose_name='Town')),
                ('annee_scolaire', models.CharField(max_length=9, verbose_name='Année Scolaire')),
                ('logo', models.URLField(blank=True, max_length=1024, null=True, verbose_name='URL du Logo')),
                ('type_enseignement', models.CharField(choices=[('technique', 'Enseignement Technique'), ('bilingue', 'Enseignement Bilingue'), ('general', 'Enseignement Général')], default='general', max_length=20, verbose_name="Type d'Enseignement")),
            ],
        ),
    ]
