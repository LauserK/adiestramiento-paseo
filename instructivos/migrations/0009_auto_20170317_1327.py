# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-03-17 17:27
from __future__ import unicode_literals

from django.db import migrations
import froala_editor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('instructivos', '0008_auto_20170317_1103'),
    ]

    operations = [
        migrations.AlterField(
            model_name='material',
            name='contenido',
            field=froala_editor.fields.FroalaField(blank=True, null=True),
        ),
    ]
