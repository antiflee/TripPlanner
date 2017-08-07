# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-07-13 00:03
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0009_auto_20170712_2003'),
    ]

    operations = [
        migrations.AlterField(
            model_name='trip',
            name='creator',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='creator', to=settings.AUTH_USER_MODEL),
        ),
    ]
