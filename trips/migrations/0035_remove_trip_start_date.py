# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-29 19:50
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0034_placevisited_encoded_polyline'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='trip',
            name='start_date',
        ),
    ]
