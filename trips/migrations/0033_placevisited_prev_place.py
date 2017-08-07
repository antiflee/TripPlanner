# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-28 19:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0032_remove_placevisited_prev_place'),
    ]

    operations = [
        migrations.AddField(
            model_name='placevisited',
            name='prev_place',
            field=models.ForeignKey(default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='next_place', to='trips.PlaceVisited'),
        ),
    ]
