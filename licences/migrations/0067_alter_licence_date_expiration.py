# Generated by Django 5.0.7 on 2024-08-15 15:50

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licences', '0066_alter_licence_date_expiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licence',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2025, 8, 15, 15, 50, 28, 839215, tzinfo=datetime.timezone.utc)),
        ),
    ]
