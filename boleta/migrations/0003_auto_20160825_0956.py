# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-25 15:56
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0002_pruebas'),
        ('boleta', '0002_auto_20160825_0008'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boletaspruebas',
            name='kit_prueba_tamizaje',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='general.Pruebas'),
        ),
    ]
