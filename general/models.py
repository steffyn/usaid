from __future__ import unicode_literals

from django.db import models
TIPO_ESTABLECIMIENTO = {
	1, "Primer Nivel",
	2, "Segundo Nivel"
}


PROVEEDORES = {
	1, "Público",
	2, "No Público"
}
GENERO = {
	1, "Hombre",
	2, "Mujer",
}
class Departamentos(models.Model):
	nombre = models.CharField(max_length=50)

class Municipios(models.Model):
	nombre = models.CharField(max_length=50)
	codigo = models.CharField(max_length=5)
	departamento = models.ForeignKey(Departamentos)

class Ciudades(models.Model):
	nombre = models.CharField(max_length=250)
	codigo = models.CharField(max_length=5)
	departamento = models.ForeignKey(Departamentos, related_name='departamento_ciudades')
	municipio = models.ForeignKey(Municipio)

class Barrios(models.Model):
	nombre = models.CharField(max_length=250)
	codigo = models.CharField(max_length=5)
	departamento = models.ForeignKey(Departamentos, related_name='departamento_barrios')
	municipio = models.ForeignKey(Municipios)
	ciudad = models.ForeignKey(Ciudades)

class Ocupaciones(models.Model):
	nombre = models.CharField(max_length=50)
	activa = models.BoleanField(default=True)

class RPN(models.Model):
	identidad = models.CharField(max_length=13)
	primer_nombre = models.CharField(max_length=50)
	segundo_nombre = models.CharField(max_length=50)
	primer_apellido = models.CharField(max_length=50)
	segundo_apellido = models.CharField(max_length=50)
	fecha_nacimiento = models.DateField()
	sexo = models.CharField(choices=GENERO)
	estado_civil = models.CharField(choices=ESTADO_CIVIL)
	fotografia + models.ImageField()

#ESTA VA PARA BOLETAS
class ActividadesEconomicas(models.Models):
	nombre = models.CharField(max_length=255)
	activa = models.BoleanField(default=True)


class Establecimientos(models.Model):
    codigo = models.CharField(max_length=10, blank=True, null=True)
    nombre = models.CharField(max_length=100, blank=True, null=True)
    departamento =  models.ForeignKey(Municipios)
    municipio =  models.ForeignKey(Municipios)
    referencia = models.CharField(max_length=500, blank=True, null=True)
    telefono = models.CharField( max_length=10, blank=True, null=True)
    tipo_establecimiento = models.IntegerField(choices=TIPO_ESTABLECIMIENTO, blank=True, null=True)
    proveedor = models.IntegerField(choices=PROVEEDORES, blank=True, null=True)
    region_sanitaria = models.CharField(max_length=1000, blank=True, null=True)
    publico = models.NullBooleanField()


class Responsables(models.Model):
    nombres = models.CharField(max_length=50)
    primer_apellido = models.CharField(max_length=50)
    segundo_apellido = models.CharField(max_length=50, blank=True, null=True)
    fecha_nacimiento = models.CharField(max_length=10)
    sexo = models.IntegerField(choices=GENERO)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono_fijo = models.CharField(max_length=10, blank=True, null=True)
    telefono_celular = models.CharField(max_length=10, blank=True, null=True)
    usuario_sistema = ForeignKey(User)
    establecimiento = ForeignKey(Establecimientos)
    activo = models.BooleanField(default=True)
