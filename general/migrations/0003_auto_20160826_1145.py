# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-26 17:45
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0002_pruebas'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rpn',
            name='fecha_nacimiento',
            field=models.DateField(verbose_name='Fecha de Nacimiento'),
        ),
    ]
