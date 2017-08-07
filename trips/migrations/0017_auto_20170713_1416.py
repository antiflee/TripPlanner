# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-13 18:16
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0016_trip_people_liked_this'),
    ]

    operations = [
        migrations.AlterField(
            model_name='placevisited',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.Trip'),
        ),
    ]
