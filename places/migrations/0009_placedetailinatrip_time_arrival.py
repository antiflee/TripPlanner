# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-08-01 03:06
from __future__ import unicode_literals

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('places', '0008_auto_20170719_2245'),
    ]

    operations = [
        migrations.AddField(
            model_name='placedetailinatrip',
            name='time_arrival',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
