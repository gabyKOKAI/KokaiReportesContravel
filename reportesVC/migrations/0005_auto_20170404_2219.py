# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-04-05 03:19
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportesVC', '0004_auto_20170404_1624'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ejecucionreporte',
            name='estatus',
            field=models.CharField(default='', max_length=10),
        ),
        migrations.AlterField(
            model_name='ejecucionreporte',
            name='nombreArchivo',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='ejecucionreporte',
            name='nombreZip',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='ejecucionreporte',
            name='rutaArchivo',
            field=models.CharField(default='', max_length=50),
        ),
    ]
