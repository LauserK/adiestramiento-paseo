# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-04-18 13:08
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='isAdmin',
            field=models.BooleanField(default=False),
        ),
    ]