# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-17 12:15
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_examenaprobado'),
    ]

    operations = [
        migrations.AlterField(
            model_name='userprofile',
            name='conceptos_aprobados',
            field=models.ManyToManyField(blank=True, to='instructivos.Concepto'),
        ),
    ]