# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-05-03 23:16
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('reportesVC', '0006_auto_20170406_2325'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ejecucionreporte',
            name='rutaArchivo',
            field=models.CharField(default='', max_length=100),
        ),
    ]