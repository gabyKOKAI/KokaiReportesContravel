# -*- coding: utf-8 -*-
# Generated by Django 1.10.6 on 2017-12-15 15:31
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('reportesVC', '0012_auto_20170704_1524'),
    ]

    operations = [
        migrations.AddField(
            model_name='ejecucionreporte',
            name='user',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
