# Generated by Django 5.0.7 on 2024-08-13 21:52

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licences', '0041_alter_licence_date_expiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licence',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2025, 8, 13, 21, 52, 3, 361418, tzinfo=datetime.timezone.utc)),
        ),
    ]
