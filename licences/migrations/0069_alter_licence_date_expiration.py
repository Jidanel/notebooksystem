# Generated by Django 5.0.7 on 2024-08-15 18:53

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('licences', '0068_alter_licence_date_expiration'),
    ]

    operations = [
        migrations.AlterField(
            model_name='licence',
            name='date_expiration',
            field=models.DateTimeField(default=datetime.datetime(2025, 8, 15, 18, 53, 43, 642875, tzinfo=datetime.timezone.utc)),
        ),
    ]
