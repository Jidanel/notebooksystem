# Generated by Django 5.0.7 on 2024-08-16 21:05

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licences', '0085_alter_licence_date_expiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licence',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2025, 8, 16, 21, 5, 40, 306158, tzinfo=datetime.timezone.utc)),
        ),
    ]
