# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 01:37
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0026_auto_20170725_2005'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='trip',
            options={'ordering': ['-created_time']},
        ),
        migrations.AddField(
            model_name='placevisited',
            name='custome_name',
            field=models.CharField(blank=True, max_length=140),
        ),
    ]
