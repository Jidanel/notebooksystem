# Generated by Django 5.0.7 on 2024-08-14 10:24

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licences', '0050_alter_licence_date_expiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licence',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2025, 8, 14, 10, 24, 47, 484197, tzinfo=datetime.timezone.utc)),
        ),
    ]