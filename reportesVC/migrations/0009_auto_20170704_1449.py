# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-07-04 19:49
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('reportesVC', '0008_tiporeporte_nombrelargo'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='ejecucionreporte',
            options={'permissions': (('can_run_Report', 'Ejecuta Reporte'),)},
        ),
    ]
