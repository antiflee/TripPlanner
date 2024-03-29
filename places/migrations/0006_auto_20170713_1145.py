# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-13 15:45
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0013_auto_20170713_1145'),
        ('places', '0005_auto_20170712_1932'),
    ]

    operations = [
        migrations.CreateModel(
            name='PlaceDetailInATrip',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expense', models.DecimalField(decimal_places=2, default=0, max_digits=7)),
                ('comment', models.CharField(blank=True, max_length=140)),
                ('lat', models.DecimalField(decimal_places=7, default=0, max_digits=10)),
                ('lng', models.DecimalField(decimal_places=7, default=0, max_digits=10)),
                ('rating', models.IntegerField(default=0)),
            ],
        ),
        migrations.RemoveField(
            model_name='placedetailintrip',
            name='place',
        ),
        migrations.RemoveField(
            model_name='placedetailintrip',
            name='trip',
        ),
        migrations.RemoveField(
            model_name='place',
            name='lat',
        ),
        migrations.RemoveField(
            model_name='place',
            name='lng',
        ),
        migrations.AlterField(
            model_name='place',
            name='associated_trips',
            field=models.ManyToManyField(blank=True, related_name='abstracted_place_list', through='places.PlaceDetailInATrip', to='trips.Trip'),
        ),
        migrations.DeleteModel(
            name='PlaceDetailInTrip',
        ),
        migrations.AddField(
            model_name='placedetailinatrip',
            name='place',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='places.Place'),
        ),
        migrations.AddField(
            model_name='placedetailinatrip',
            name='trip',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='trips.Trip'),
        ),
    ]
