# Generated by Django 5.0.7 on 2024-08-18 08:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licences', '0091_alter_licence_date_expiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licence',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2025, 8, 18, 8, 5, 40, 356128, tzinfo=datetime.timezone.utc)),
        ),
    ]
