# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-02 11:54
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructivos', '0005_auto_20170301_1519'),
    ]

    operations = [
        migrations.AddField(
            model_name='concepto',
            name='activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='examen',
            name='activo',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='material',
            name='activo',
            field=models.BooleanField(default=False),
        ),
    ]