from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from general.models import *

POBLACIONES = (
	(1, "Poblacion General"),
	(2, "HSH"),
	(3, "Trabajador(a) Sexual"),
	(4, "Transgenero	"),
)

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

GRUPO_ETNICO = (
	(1, "Mestizo"),
	(2, "Misquito"),
	(3, "Pech"),
	(4, "Maya Chorti"),
	(5, "Tawahka"),
	(6, "Garifuna"),
	(7, "Negro de Habla Inglesa"),
	(8, "Lenca"),
	(9, "Tolupan"),
	(1, "Otro"),
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

class Boletas(models.Model):
	establecimiento = models.IntegerField(choices=TIPO_ESTABLECIMIENTO)
	identidad = models.CharField(max_length=13)
	expediente = models.CharField(max_length=50, blank=True, null=True)
	sexo = models.IntegerField(choices=GENERO)
	edad_anios = models.IntegerField()
	edad_meses = models.IntegerField()
	pseudonimo = models.IntegerField(choices=GENERO, blank=True, null=True)
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
	grupo_etnico = models.IntegerField(choices=GRUPO_ETNICO)
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
	poblacion = models.IntegerField(choices=POBLACIONES, blank=True, null=True)
	actividad_economica = models.ForeignKey(ActividadesEconomicas, blank=True, null=True)
	fecha_ultima_menstruacion = models.CharField(max_length=10, blank=True, null=True) 
	ciudad = models.ForeignKey(Ciudades, related_name='boleta_origen_ciudades')
	barrio = models.ForeignKey(Ciudades, related_name='boleta_origen_barrios', blank=True, null=True)
	rnp = models.NullBooleanField()
	creado_por = models.ForeignKey(User, related_name='creado_por_boleta')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	actualizado_por = models.ForeignKey(User, related_name='actualizado_por_boleta')
	fecha_actualizacion = models.DateTimeField(auto_now=True)


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

