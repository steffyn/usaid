# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-31 05:21
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('general', '0003_auto_20160826_1145'),
        ('boleta', '0007_auto_20160826_1145'),
    ]

    operations = [
        migrations.CreateModel(
            name='Asistencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('lugar', models.IntegerField(choices=[(1, 'San Pedro Sula'), (2, 'La Ceiba'), (3, 'Tegucigalpa'), (4, 'Puerto Cortes'), (5, 'Tela')])),
                ('actividad', models.CharField(max_length=200)),
                ('poblacion', models.IntegerField(choices=[(1, 'MTS'), (2, 'HSH/TG')])),
                ('intervencion', models.IntegerField(choices=[(1, 'Proveer o referir a Servicios de Consejeria y Prueba'), (2, 'Promocion y Distribucion de Condones y Lubricantes'), (3, 'Referencia a Tamizaje, Prevencion y Tratamiento de ITS'), (4, 'Difusion/Alcance y Empoderamiento'), (5, 'Abordaje para IEC'), (6, 'Referencia Salud Reproductiva (Planificacion Familiar)')])),
                ('responsable', models.CharField(blank=True, max_length=100, null=True)),
                ('coordinador', models.CharField(blank=True, max_length=100, null=True)),
                ('establecimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Establecimientos')),
            ],
        ),
        migrations.CreateModel(
            name='ListadoAsistencia',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identidad', models.CharField(max_length=13)),
                ('nombres', models.CharField(max_length=255)),
                ('correo_electronico', models.CharField(blank=True, max_length=150, null=True)),
                ('edad', models.IntegerField()),
                ('telefono', models.CharField(max_length=10)),
                ('cantidad_condones', models.IntegerField()),
                ('asistencia', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='boleta.Asistencia')),
            ],
        ),
        migrations.AlterField(
            model_name='boletaspruebas',
            name='fecha_extraccion',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Estracci\xf3n'),
        ),
        migrations.AlterField(
            model_name='boletaspruebas',
            name='fecha_muestra',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Recepci\xf3n de Muestra'),
        ),
        migrations.AlterField(
            model_name='boletaspruebas',
            name='fecha_prueba',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha en que se Realiz\xf3 la Prueba'),
        ),
        migrations.AlterField(
            model_name='boletaspruebas',
            name='fecha_prueba_confirmatoria',
            field=models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Prueba Confirmatoria'),
        ),
        migrations.AlterField(
            model_name='boletaspruebas',
            name='kit_prueba_tamizaje',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='kit_tamizaje', to='general.Pruebas', verbose_name='Kit Utilizado en Prueba Tamizaje'),
        ),
        migrations.AlterField(
            model_name='boletaspruebas',
            name='nombre_persona_prueba',
            field=models.CharField(blank=True, max_length=255, null=True, verbose_name='Nombre de Persona que Realiz\xf3 la prueba'),
        ),
        migrations.AlterField(
            model_name='boletaspruebas',
            name='numero_prueba',
            field=models.IntegerField(blank=True, null=True, verbose_name='N\xfamero de Prueba'),
        ),
        migrations.AlterField(
            model_name='boletaspruebas',
            name='resultado_prueba_tamizaje',
            field=models.IntegerField(blank=True, null=True, verbose_name='Resultado de Prueba Tamizaje'),
        ),
    ]