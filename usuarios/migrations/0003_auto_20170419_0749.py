# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-19 11:49
from __future__ import unicode_literals

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0002_userprofile_isadmin'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='cedula',
            field=models.CharField(blank=True, default=b'', max_length=10),
        ),
        migrations.AlterField(
            model_name='examenaprobado',
            name='nota',
            field=models.IntegerField(default=0, validators=[django.core.validators.MaxValueValidator(20), django.core.validators.MinValueValidator(0)]),
        ),
    ]