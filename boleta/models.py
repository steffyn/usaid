# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from general.models import *

PERIOSIDAD = (
	(1, "Primera Vez"),
	(2, "Subsiguiente"),
)

GENERO = (
	(1, "Hombre"),
	(2, "Mujer"),
)

ESTADO_CIVIL = (
	(1, "Soltero(a)"),
	(2, "Casado(a)"),
	(3, "Union Libre"),
)


PROVEEDORES = (
	(1, "Publico"),
	(2, "No Publico"),
)

TIPO_ESTABLECIMIENTO = (
	(1, "Primer Nivel"),
	(2, "Segundo Nivel"),
)

#ESTA VA PARA BOLETAS
class Condiciones(models.Model):
	nombre = models.CharField(max_length=255)
	orden = models.IntegerField()
	activa = models.BooleanField(default=True)
	def __unicode__(self):
		return u'%s' % (self.nombre)

class Boletas(models.Model):
	establecimiento = models.IntegerField(choices=TIPO_ESTABLECIMIENTO)
	identidad = models.CharField(max_length=13)
	expediente = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número de Expediente Clínico o Código Identificador Único:")
	sexo = models.IntegerField(choices=GENERO)
	edad_anios = models.IntegerField(verbose_name="Anios")
	edad_meses = models.IntegerField(verbose_name="Meses")
	pseudonimo = models.CharField(max_length=150, blank=True, null=True)
	estado_civil = models.IntegerField(choices=ESTADO_CIVIL)
	telefono_fijo = models.CharField(max_length=10, blank=True, null=True)
	telefono_celular = models.CharField(max_length=10, blank=True, null=True)
	ocupacion = models.ForeignKey(Ocupaciones)
	departamento = models.ForeignKey(Departamentos)
	municipio = models.ForeignKey(Municipios)
	calle = models.CharField(max_length=100, blank=True, null=True)
	bloque = models.CharField(max_length=10, blank=True, null=True)
	numero_casa = models.CharField(max_length=10, blank=True, null=True)
	referencias = models.CharField(max_length=500, blank=True, null=True)
	grupo_etnico = models.ForeignKey(GruposEtnicos)
	otro_grupo_etnico = models.CharField(max_length=50, blank=True, null=True)
	identidad_madre = models.CharField(max_length=13, blank=True, null=True)
	nombre_madre = models.CharField(max_length=150, blank=True, null=True)
	telefono_madre = models.CharField(max_length=10, blank=True, null=True)
	identidad_padre = models.CharField(max_length=13, blank=True, null=True)
	nombre_padre = models.CharField(max_length=150, blank=True, null=True)
	telefono_padre = models.CharField(max_length=10, blank=True, null=True)
	identidad_tutor = models.CharField(max_length=13, blank=True, null=True)
	nombre_tutor = models.CharField(max_length=150, blank=True, null=True)
	telefono_tutor = models.CharField(max_length=10, blank=True, null=True)
	direccion_tutor = models.CharField(max_length=500, blank=True, null=True)
	poblacion = models.ForeignKey(Poblaciones, blank=True, null=True)
	actividad_economica = models.ForeignKey(ActividadesEconomicas, blank=True, null=True)
	fecha_ultima_menstruacion = models.CharField(max_length=10, blank=True, null=True) 
	ciudad = models.ForeignKey(Ciudades, related_name='boleta_origen_ciudades')
	barrio = models.ForeignKey(Ciudades, related_name='boleta_origen_barrios', blank=True, null=True)
	rnp = models.NullBooleanField()
	creado_por = models.ForeignKey(User, related_name='creado_por_boleta')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	actualizado_por = models.ForeignKey(User, related_name='actualizado_por_boleta')
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	condiciones = models.ManyToManyField(Condiciones)

	def __unicode__(self):
		return u'%s' % (self.identidad)

class BoletasConsejeria(models.Model):
	boleta = models.ForeignKey(Boletas)
	fecha_consejeria = models.CharField(max_length=10, blank=True, null=True)
	periodicidad = models.IntegerField(blank=True, null=True)
	nombre_persona_solicitante = models.CharField(max_length=150, blank=True, null=True)
	nombre_consejero = models.CharField(max_length=150, blank=True, null=True)
	creado_por = models.ForeignKey(User, related_name='creado_por_boleta_consejeria')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	actualizado_por = models.ForeignKey(User, related_name='actualizado_por_boleta_consejeria')
	fecha_actualizacion = models.DateTimeField(auto_now=True)



class BoletasConsejeriaPostPrueba(models.Model):
	boleta = models.ForeignKey(Boletas)
	fecha_consejeria = models.CharField(max_length=10, blank=True, null=True)
	nombre_consejero = models.CharField(max_length=150, blank=True, null=True)
	observaciones = models.CharField(max_length=255, blank=True, null=True)
	creado_por = models.ForeignKey(User, related_name='creado_por_boleta_postprueba')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	actualizado_por = models.ForeignKey(User, related_name='actualizado_por_boleta_postprueba')
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	referido =models.CharField(max_length=255, blank=True, null=True)

class BoletasObservaciones(models.Model):
	boleta = models.ForeignKey(Boletas)
	establecimiento = models.ForeignKey(Establecimientos)
	nombre_consejero = models.CharField(max_length=150)
	observaciones = models.CharField(max_length=255)
	tipo_observacion = models.IntegerField(blank=True, null=True)
	creado_por = models.ForeignKey(User, related_name='creado_por_boleta_obs')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	actualizado_por = models.ForeignKey(User, related_name='actualizado_por_boleta_obs')
	fecha_actualizacion = models.DateTimeField(auto_now=True)

class BoletasPruebas(models.Model):
	boleta = models.ForeignKey(Boletas)
	fecha_solicitud = models.DateTimeField(blank=True, null=True)
	numero_prueba = models.IntegerField(blank=True, null=True)
	fecha_extraccion = models.DateTimeField(blank=True, null=True)
	fecha_muestra = models.DateTimeField(blank=True, null=True)
	fecha_prueba = models.DateTimeField(blank=True, null=True)
	kit_prueba_tamizaje = models.ForeignKey(Pruebas, blank=True, null=True, related_name='kit_tamizaje')
	resultado_prueba_tamizaje = models.IntegerField(blank=True, null=True)
	nombre_persona_prueba = models.CharField(max_length=255, blank=True, null=True)
	fecha_prueba_confirmatoria = models.DateTimeField(blank=True, null=True)
	kit_prueba_confirmatoria = models.ForeignKey(Pruebas, blank=True, null=True, related_name='kit_confirmatoria')
	institucion_prueba_confirmatoria = models.IntegerField( blank=True, null=True)
	resultado_prueba_confirmatoria = models.IntegerField( blank=True, null=True)
	nombre_laboratorio = models.CharField(max_length=255, blank=True, null=True)
	fecha_refirio_prueba_confirmatoria = models.DateTimeField(blank=True, null=True)

	creado_por = models.ForeignKey(User, related_name='creado_por_boleta_prueba')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	actualizado_por = models.ForeignKey(User, related_name='actualizado_por_boleta_prueba')
	fecha_actualizacion = models.DateTimeField(auto_now=True)

