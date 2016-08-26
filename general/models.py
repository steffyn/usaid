from __future__ import unicode_literals
from django.db import models
from django.contrib.auth.models import User

TIPO_ESTABLECIMIENTO = (
	(1, "Primer Nivel"),
	(2, "Segundo Nivel"),
)

PROVEEDORES = (
	(1, "Publico"),
	(2, "No Publico"),
)

GENERO = (
	(1, "Hombre",),
	(2, "Mujer"),
)

ESTADO_CIVIL = (
	(1, "Soltero(a)"),
	(2, "Casado(a)"),
	(3, "Union Libre"),
)
class Departamentos(models.Model):
	nombre = models.CharField(max_length=50)
	codigo = models.CharField(max_length=5)

	def __unicode__(self):
		return u'%s - %s' % (self.codigo, self.nombre)

class Municipios(models.Model):
	nombre = models.CharField(max_length=50)
	codigo = models.CharField(max_length=5)
	departamento = models.ForeignKey(Departamentos)

	def __unicode__(self):
		return u'%s - %s' % (self.codigo, self.nombre)

class Ciudades(models.Model):
	nombre = models.CharField(max_length=250)
	codigo = models.CharField(max_length=5)
	departamento = models.ForeignKey(Departamentos, related_name='departamento_ciudades')
	municipio = models.ForeignKey(Municipios, related_name='municipios_ciudades')

	def __unicode__(self):
		return u'%s - %s' % (self.codigo, self.nombre)

class Barrios(models.Model):
	nombre = models.CharField(max_length=250)
	codigo = models.CharField(max_length=5)
	departamento = models.ForeignKey(Departamentos, related_name='barrio_origen_departamento')
	municipio = models.ForeignKey(Municipios, related_name="barrio_origen_municipio")
	ciudad = models.ForeignKey(Ciudades, related_name="barrio_origen_ciudad")

	def __unicode__(self):
		return u'%s - %s' % (self.codigo, self.nombre)

class Ocupaciones(models.Model):
	nombre = models.CharField(max_length=50)
	activa = models.BooleanField(default=True)

	def __unicode__(self):
		return u'%s' % (self.nombre)

class RPN(models.Model):
	identidad = models.CharField(max_length=13)
	primer_nombre = models.CharField(max_length=50)
	segundo_nombre = models.CharField(max_length=50,  blank=True, null=True)
	primer_apellido = models.CharField(max_length=50)
	segundo_apellido = models.CharField(max_length=50,  blank=True, null=True)
	fecha_nacimiento = models.DateField(verbose_name='Fecha de Nacimiento')
	sexo = models.IntegerField(choices=GENERO)
	estado_civil = models.IntegerField(choices=ESTADO_CIVIL)
	fotografia = models.ImageField( blank=True, null=True)

	def __unicode__(self):
		return u'[%s] %s %s' % (self.identidad, self.primer_nombre, self.primer_apellido)

#ESTA VA PARA BOLETAS
class ActividadesEconomicas(models.Model):
	nombre = models.CharField(max_length=255)
	activa = models.BooleanField(default=True)
	def __unicode__(self):
		return u'%s' % (self.nombre)

class Establecimientos(models.Model):
	codigo = models.CharField(max_length=10, blank=True, null=True)
	nombre = models.CharField(max_length=100, blank=True, null=True)
	departamento =  models.ForeignKey(Departamentos, related_name='establecimiento_origen_departamento')
	municipio =  models.ForeignKey(Municipios, related_name='establecimiento_origen_municipio')
	referencia = models.CharField(max_length=500, blank=True, null=True)
	telefono = models.CharField( max_length=10, blank=True, null=True)
	tipo_establecimiento = models.IntegerField(choices=TIPO_ESTABLECIMIENTO, blank=True, null=True)
	proveedor = models.IntegerField(choices=PROVEEDORES, blank=True, null=True)
	region_sanitaria = models.CharField(max_length=1000, blank=True, null=True)
	publico = models.NullBooleanField()

	def __unicode__(self):
		return u'%s' % (self.nombre)


class Responsables(models.Model):
	nombres = models.CharField(max_length=50)
	primer_apellido = models.CharField(max_length=50)
	segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
	fecha_nacimiento = models.DateField(max_length=10)
	sexo = models.IntegerField(choices=GENERO)
	direccion = models.CharField(max_length=255, blank=True, null=True)
	telefono_fijo = models.CharField(max_length=10, blank=True, null=True)
	telefono_celular = models.CharField(max_length=10, blank=True, null=True)
	usuario_sistema = models.ForeignKey(User)
	establecimiento = models.ForeignKey(Establecimientos)
	activo = models.BooleanField(default=True)

	def __unicode__(self):
		return u'%s %s' % (self.nombres, self.primer_apellido)

class GruposEtnicos(models.Model):
	nombre = models.CharField(max_length=50) 
	activo = models.BooleanField(default=True) 
	def __unicode__(self):
		return u'%s' % (self.nombre)

class Poblaciones(models.Model):
	nombre = models.CharField(max_length=50)
	orden = models.IntegerField()
	activo = models.BooleanField(default=True)

	def __unicode__(self):
		return u'%s' % (self.nombre)

class Pruebas(models.Model):
	nombre = models.CharField(max_length=255)
	tipo = models.IntegerField()
	activo = models.BooleanField(default=True)

	def __unicode__(self):
		return u'%s' % (self.nombre)
