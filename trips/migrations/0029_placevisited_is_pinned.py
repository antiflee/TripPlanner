# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-26 13:17
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0028_auto_20170725_2204'),
    ]

    operations = [
        migrations.AddField(
            model_name='placevisited',
            name='is_pinned',
            field=models.BooleanField(default=False),
        ),
    ]
