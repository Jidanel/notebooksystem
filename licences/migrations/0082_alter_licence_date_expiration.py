# Generated by Django 5.0.7 on 2024-08-16 16:16

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licences', '0081_alter_licence_date_expiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licence',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2025, 8, 16, 16, 15, 55, 177162, tzinfo=datetime.timezone.utc)),
        ),
    ]
