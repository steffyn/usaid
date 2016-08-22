from __future__ import unicode_literals

from django.db import models

POBLACIONES = {
	1, "Población General",
	2, "HSH",
	3, "Trabajador(a) Sexual",
	4, "Transgénero	",
}

PERIOSIDAD = {
	1, "Primera Vez",
	2, "Subsiguiente",
}

GENERO = {
	1, "Hombre",
	2, "Mujer",
}

ESTADO_CIVIL = {
	1, "Soltero(a)",
	2, "Casado(a)",
	3, "Unión Libre",
}

GRUPO_ETNICO = {
	1, "Mestizo",
	2, "Misquito",
	3, "Pech",
	4, "Maya Chorti",
	5, "Tawahka",
	6, "Garifuna",
	7, "Negro de Habla Inglesa",
	8, "Lenca",
	9, "Tolupan",
	1, "Otro",
}

PROVEEDORES = {
	1, "Público",
	2, "No Público"
}

TIPO_ESTABLECIMIENTO = {
	1, "Primer Nivel",
	2, "Segundo Nivel"
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
	activa + models.BoleanField(default=True)

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
class Condiciones(models.Models):
	nombre = models.CharField(max_length=255)
	orden = models.IntegerField()
	activa = models.BoleanField(default=True)

