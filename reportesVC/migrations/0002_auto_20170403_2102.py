# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-04 02:02
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reportesVC', '0001_initial'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='MesesReporte',
            new_name='MesReporte',
        ),
        migrations.RenameField(
            model_name='mesreporte',
            old_name='mes',
            new_name='nombre',
        ),
        migrations.RenameField(
            model_name='tiporeporte',
            old_name='tipo',
            new_name='nombre',
        ),
    ]
