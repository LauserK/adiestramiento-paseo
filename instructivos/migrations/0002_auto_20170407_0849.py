# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-07 12:49
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('instructivos', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='examen',
            name='ilustracion',
        ),
        migrations.AddField(
            model_name='pregunta',
            name='ilustracion',
            field=models.ImageField(blank=True, default='', upload_to='examenes/'),
        ),
    ]
