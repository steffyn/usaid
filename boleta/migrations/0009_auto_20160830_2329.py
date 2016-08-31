# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 05:29
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('boleta', '0008_auto_20160830_2321'),
    ]

    operations = [
        migrations.AddField(
            model_name='asistencia',
            name='fecha_creacion',
            field=models.DateTimeField(auto_now_add=True, default='2010-01-01'),
            preserve_default=False,
        ),
    ]
