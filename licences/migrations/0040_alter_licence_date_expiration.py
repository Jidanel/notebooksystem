# Generated by Django 5.0.7 on 2024-08-13 17:03

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licences', '0039_alter_licence_date_expiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licence',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2025, 8, 13, 17, 3, 47, 898386, tzinfo=datetime.timezone.utc)),
        ),
    ]
