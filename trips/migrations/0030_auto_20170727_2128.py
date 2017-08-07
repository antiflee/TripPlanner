# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-28 01:28
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0029_placevisited_is_pinned'),
    ]

    operations = [
        migrations.AddField(
            model_name='placevisited',
            name='tag_color',
            field=models.CharField(choices=[('label label-primary', 'label label-primary'), ('label label-success', 'label label-success'), ('label label-info', 'label label-info'), ('label label-warning', 'label label-warning'), ('label label-danger', 'label label-danger'), ('label label-default', 'label label-default')], default='label label-primary', max_length=20),
        ),
        migrations.AlterField(
            model_name='placevisited',
            name='travel_mode_to_here',
            field=models.CharField(choices=[('Driving', 'DRIVING'), ('Transit', 'TRANSIT'), ('Walking', 'WALKING'), ('Cycling', 'BICYCLING'), ('START', 'START')], default='START', max_length=9),
        ),
    ]
