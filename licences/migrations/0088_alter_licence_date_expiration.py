# Generated by Django 5.0.7 on 2024-08-17 08:27

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licences', '0087_alter_licence_date_expiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licence',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2025, 8, 17, 8, 27, 26, 624121, tzinfo=datetime.timezone.utc)),
        ),
    ]
