# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-12 23:32
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0007_auto_20170710_1515'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='placevisited',
            name='place',
        ),
        migrations.RemoveField(
            model_name='trip',
            name='places',
        ),
        migrations.AddField(
            model_name='placevisited',
            name='displayed_name',
            field=models.CharField(blank=True, max_length=140),
        ),
        migrations.AddField(
            model_name='placevisited',
            name='lat',
            field=models.DecimalField(decimal_places=7, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='placevisited',
            name='lng',
            field=models.DecimalField(decimal_places=7, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='placevisited',
            name='travel_dist_to_here_meter',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='placevisited',
            name='travel_dist_to_here_text',
            field=models.CharField(blank=True, max_length=140),
        ),
        migrations.AddField(
            model_name='placevisited',
            name='travel_time_to_here_sec',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='placevisited',
            name='travel_time_to_here_text',
            field=models.CharField(blank=True, max_length=140),
        ),
        migrations.AddField(
            model_name='trip',
            name='time_on_travel_hours',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AddField(
            model_name='trip',
            name='total_duration_days',
            field=models.PositiveIntegerField(default=0),
        ),
        migrations.AlterField(
            model_name='placevisited',
            name='travel_mode_to_here',
            field=models.CharField(choices=[('Driving', 'DRIVING'), ('Transit', 'TRANSIT'), ('Walking', 'WALKING'), ('Cycling', 'BICYCLING'), ('Flight', 'FLIGHT'), ('START', 'START')], default='START', max_length=9),
        ),
        migrations.AlterField(
            model_name='placevisited',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='places', to='trips.Trip'),
        ),
    ]
