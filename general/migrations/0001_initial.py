# -*- coding: utf-8 -*-
# Generated by Django 1.10 on 2016-08-24 06:13
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ActividadesEconomicas',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=255)),
                ('activa', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Barrios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('codigo', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Ciudades',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=250)),
                ('codigo', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Departamentos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('codigo', models.CharField(max_length=5)),
            ],
        ),
        migrations.CreateModel(
            name='Establecimientos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('codigo', models.CharField(blank=True, max_length=10, null=True)),
                ('nombre', models.CharField(blank=True, max_length=100, null=True)),
                ('referencia', models.CharField(blank=True, max_length=500, null=True)),
                ('telefono', models.CharField(blank=True, max_length=10, null=True)),
                ('tipo_establecimiento', models.IntegerField(blank=True, choices=[(1, 'Primer Nivel'), (2, 'Segundo Nivel')], null=True)),
                ('proveedor', models.IntegerField(blank=True, choices=[(1, 'Publico'), (2, 'No Publico')], null=True)),
                ('region_sanitaria', models.CharField(blank=True, max_length=1000, null=True)),
                ('publico', models.NullBooleanField()),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='establecimiento_origen_departamento', to='general.Departamentos')),
            ],
        ),
        migrations.CreateModel(
            name='GruposEtnicos',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Municipios',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('codigo', models.CharField(max_length=5)),
                ('departamento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Departamentos')),
            ],
        ),
        migrations.CreateModel(
            name='Ocupaciones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('activa', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Poblaciones',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('orden', models.IntegerField()),
                ('activo', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Responsables',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombres', models.CharField(max_length=50)),
                ('primer_apellido', models.CharField(max_length=50)),
                ('segundo_apellido', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha_nacimiento', models.DateField(max_length=10)),
                ('sexo', models.IntegerField(choices=[(1, 'Hombre'), (2, 'Mujer')])),
                ('direccion', models.CharField(blank=True, max_length=255, null=True)),
                ('telefono_fijo', models.CharField(blank=True, max_length=10, null=True)),
                ('telefono_celular', models.CharField(blank=True, max_length=10, null=True)),
                ('activo', models.BooleanField(default=True)),
                ('establecimiento', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='general.Establecimientos')),
                ('usuario_sistema', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='RPN',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identidad', models.CharField(max_length=13)),
                ('primer_nombre', models.CharField(max_length=50)),
                ('segundo_nombre', models.CharField(blank=True, max_length=50, null=True)),
                ('primer_apellido', models.CharField(max_length=50)),
                ('segundo_apellido', models.CharField(blank=True, max_length=50, null=True)),
                ('fecha_nacimiento', models.DateField()),
                ('sexo', models.IntegerField(choices=[(1, 'Hombre'), (2, 'Mujer')])),
                ('estado_civil', models.IntegerField(choices=[(1, 'Soltero(a)'), (2, 'Casado(a)'), (3, 'Union Libre')])),
                ('fotografia', models.ImageField(blank=True, null=True, upload_to=b'')),
            ],
        ),
        migrations.AddField(
            model_name='establecimientos',
            name='municipio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='establecimiento_origen_municipio', to='general.Municipios'),
        ),
        migrations.AddField(
            model_name='ciudades',
            name='departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='departamento_ciudades', to='general.Departamentos'),
        ),
        migrations.AddField(
            model_name='ciudades',
            name='municipio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='municipios_ciudades', to='general.Municipios'),
        ),
        migrations.AddField(
            model_name='barrios',
            name='ciudad',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='barrio_origen_ciudad', to='general.Ciudades'),
        ),
        migrations.AddField(
            model_name='barrios',
            name='departamento',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='barrio_origen_departamento', to='general.Departamentos'),
        ),
        migrations.AddField(
            model_name='barrios',
            name='municipio',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='barrio_origen_municipio', to='general.Municipios'),
        ),
    ]
