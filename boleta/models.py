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

LUGARES = (
	(1, "San Pedro Sula"),
	(2, "La Ceiba"),
	(3, "Tegucigalpa"),
	(4, "Puerto Cortes"),
	(5, "Tela"),
)

TIPO_POBLACION = (
	(1, "MTS"),
	(2, "HSH/TG"),
)

SI_NO = (
	(1, "SI"),
	(2, "NO"),
)

ESTADO_INMUNOLOGICO = (
	(1, "CD4<200"),
	(2, "CD4=200-499"),
	(3, "CD4>=500"),
	(4, "N/A"),
)

ESTADIO_CLINICO = (
	("A", "A"),
	("B", "B"),
	("C", "C"),
)

TIPO_INTERVENCION = (
	(1, "Proveer o referir a Servicios de Consejeria y Prueba"),
	(2, "Promocion y Distribucion de Condones y Lubricantes"),
	(3, "Referencia a Tamizaje, Prevencion y Tratamiento de ITS"),
	(4, "Difusion/Alcance y Empoderamiento"),
	(5, "Abordaje para IEC"),
	(6, "Referencia Salud Reproductiva (Planificacion Familiar)"),
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
	primer_nombre = models.CharField(max_length=50, blank=True, null=True, verbose_name="")
	segundo_nombre = models.CharField(max_length=50, blank=True, null=True, verbose_name="")
	primer_apellido = models.CharField(max_length=50, blank=True, null=True, verbose_name="")
	segundo_apellido = models.CharField(max_length=50, blank=True, null=True, verbose_name="")
	fecha_nacimiento = models.DateField( blank=True, null=True, verbose_name="")
	expediente = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número de Expediente Clínico o Código Identificador Único:")
	sexo = models.IntegerField(choices=GENERO)
	edad_anios = models.IntegerField(verbose_name="Años")
	edad_meses = models.IntegerField(verbose_name="Meses")
	pseudonimo = models.CharField(max_length=150, blank=True, null=True, verbose_name='Nombre Social')
	estado_civil = models.IntegerField(choices=ESTADO_CIVIL, verbose_name='Estado Civil')
	telefono_fijo = models.CharField(max_length=10, blank=True, null=True, verbose_name='Teléfono Fijo')
	telefono_celular = models.CharField(max_length=10, blank=True, null=True, verbose_name='Teléfono Celular')
	ocupacion = models.ForeignKey(Ocupaciones)
	departamento = models.ForeignKey(Departamentos)
	municipio = models.ForeignKey(Municipios)
	calle = models.CharField(max_length=100, blank=True, null=True, verbose_name='Calle o Avenida')
	bloque = models.CharField(max_length=10, blank=True, null=True)
	numero_casa = models.CharField(max_length=10, blank=True, null=True, verbose_name='Número de Casa o Apartamento')
	referencias = models.CharField(max_length=500, blank=True, null=True, verbose_name='Otras Referencias')
	grupo_etnico = models.ForeignKey(GruposEtnicos, verbose_name='Grupo Étnico')
	otro_grupo_etnico = models.CharField(max_length=50, blank=True, null=True, verbose_name='Otro Grupo Étnico')
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
	poblacion = models.ForeignKey(Poblaciones, blank=True, null=True, verbose_name='Población Solicitante')
	actividad_economica = models.ForeignKey(ActividadesEconomicas, blank=True, null=True, verbose_name='Actividad Económica')
	fecha_ultima_menstruacion = models.CharField(max_length=10, blank=True, null=True) 
	ciudad = models.ForeignKey(Ciudades, related_name='boleta_origen_ciudades')
	barrio = models.ForeignKey(Ciudades, related_name='boleta_origen_barrios', blank=True, null=True, verbose_name='Barrio, Aldea, Colonia o Caserio')
	rnp = models.NullBooleanField()
	creado_por = models.ForeignKey(User, related_name='creado_por_boleta')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	actualizado_por = models.ForeignKey(User, related_name='actualizado_por_boleta')
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	condiciones = models.ManyToManyField(Condiciones, verbose_name='Condición (marque todas las que apliquen)')
	otro_condicion = models.CharField(max_length=50, blank=True, null=True, verbose_name='Otra Condición')

	def __unicode__(self):
		return u'%s' % (self.identidad)

class BoletasConsejeria(models.Model):
	boleta = models.ForeignKey(Boletas)
	periodicidad = models.IntegerField(blank=True, null=True)
	fecha_consejeria = models.CharField(max_length=10, blank=True, null=True, verbose_name='Fecha de Consejería Pre Prueba')
	nombre_persona_solicitante = models.CharField(max_length=150, blank=True, null=True, verbose_name='Nombre de la Persona Solicitante/Encargada/Responsable')
	nombre_consejero = models.CharField(max_length=150, blank=True, null=True)
	creado_por = models.ForeignKey(User, related_name='creado_por_boleta_consejeria')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	actualizado_por = models.ForeignKey(User, related_name='actualizado_por_boleta_consejeria')
	fecha_actualizacion = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return u'%s' % (self.boleta.identidad)


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
	def __unicode__(self):
		return u'%s' % (self.boleta.identidad)

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
	def __unicode__(self):
		return u'%s' % (self.boleta.identidad)

class BoletasPruebas(models.Model):
	boleta = models.ForeignKey(Boletas)
	fecha_solicitud = models.DateTimeField(blank=True, null=True)
	numero_prueba = models.IntegerField(blank=True, null=True, verbose_name='Número de Prueba')
	fecha_extraccion = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Estracción')
	fecha_muestra = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Recepción de Muestra')
	fecha_prueba = models.DateTimeField(blank=True, null=True, verbose_name='Fecha en que se Realizó la Prueba')
	kit_prueba_tamizaje = models.ForeignKey(Pruebas, blank=True, null=True, related_name='kit_tamizaje', verbose_name='Kit Utilizado en Prueba Tamizaje')
	resultado_prueba_tamizaje = models.IntegerField(blank=True, null=True, verbose_name='Resultado de Prueba Tamizaje')
	nombre_persona_prueba = models.CharField(max_length=255, blank=True, null=True, verbose_name='Nombre de Persona que Realizó la prueba')
	fecha_prueba_confirmatoria = models.DateTimeField(blank=True, null=True, verbose_name='Fecha de Prueba Confirmatoria')
	kit_prueba_confirmatoria = models.ForeignKey(Pruebas, blank=True, null=True, related_name='kit_confirmatoria')
	institucion_prueba_confirmatoria = models.IntegerField( blank=True, null=True)
	resultado_prueba_confirmatoria = models.IntegerField( blank=True, null=True)
	nombre_laboratorio = models.CharField(max_length=255, blank=True, null=True)
	fecha_refirio_prueba_confirmatoria = models.DateTimeField(blank=True, null=True)

	creado_por = models.ForeignKey(User, related_name='creado_por_boleta_prueba')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	actualizado_por = models.ForeignKey(User, related_name='actualizado_por_boleta_prueba')
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	def __unicode__(self):
		return u'%s' % (self.boleta.identidad)

class Asistencia(models.Model):
	establecimiento = models.ForeignKey(Establecimientos, verbose_name='ONG Implementadora')
	fecha = models.DateField()
	lugar = models.IntegerField(choices=LUGARES)
	actividad = models.CharField(max_length=200, verbose_name='Actividad/Tema')
	poblacion = models.IntegerField(choices=TIPO_POBLACION, verbose_name='Tipo de Población Clave Atendida')
	intervencion = models.IntegerField(choices=TIPO_INTERVENCION, verbose_name='Tipo de Intervensión')
	responsable = models.CharField(max_length=100,blank=True, null=True, verbose_name='Nombre del/la Responsable de la Actividad')
	coordinador = models.CharField(max_length=100,blank=True, null=True, verbose_name='Nombre del/la Coordinador de Proyecto')

	creado_por = models.ForeignKey(User, related_name='creado_por_asistencia')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	actualizado_por = models.ForeignKey(User, related_name='actualizado_por_asistencia')
	fecha_actualizacion = models.DateTimeField(auto_now=True)

class ListadoAsistencia(models.Model):
	asistencia = models.ForeignKey(Asistencia)
	identidad = models.CharField(max_length=13)
	nombres = models.CharField(max_length=255)
	correo_electronico = models.CharField(max_length=150, blank=True, null=True)
	edad = models.IntegerField()
	telefono = models.CharField(max_length=10)
	cantidad_condones = models.IntegerField()

class BoletaClinica(models.Model):
	boleta = models.ForeignKey(Boletas)
	relaciones_mismo_sexo = models.IntegerField(choices=SI_NO, blank=True, null=True)
	dinero_por_relaciones = models.IntegerField(choices=SI_NO, blank=True, null=True)
	identificacion_genero = models.IntegerField(choices=SI_NO, blank=True, null=True)
	embarazada_vih = models.IntegerField(choices=SI_NO, blank=True, null=True)
	fecha_ultima_menstruacion = models.DateField(blank=True, null=True)
	semanas_gestiacion = models.IntegerField(blank=True, null=True)
	evaluacion_go = models.IntegerField(choices=SI_NO, blank=True, null=True)
	programacion_cesaria = models.IntegerField(choices=SI_NO, blank=True, null=True)
	fecha_cesaria = models.DateField(blank=True, null=True)
	afiliacion_seguridad_social = models.IntegerField(choices=SI_NO, blank=True, null=True)
	clase_afiliacion =  models.CharField(max_length=200, verbose_name='Clase de Afiliacion')
	seguro_privado = models.IntegerField(choices=SI_NO, blank=True, null=True)
	nombre_aseguradora = models.CharField(max_length=200, verbose_name='Nombre de la Aseguradora Social')
	fecha_diagnostico = models.DateField(blank=True, null=True)
	fecha_primera_consulta = models.DateField(blank=True, null=True)
	fecha_proxima_cita = models.DateField(blank=True, null=True)
	cita_medica = models.CharField(max_length=200, blank=True, null=True)
	retiro_medicamento = models.CharField(max_length=200, blank=True, null=True)
	talla = models.CharField(max_length=3, blank=True, null=True)
	peso = models.CharField(max_length=3, blank=True, null=True)
	imc = models.CharField(max_length=3, blank=True, null=True)
	estado_inmunologico = models.IntegerField(choices=ESTADO_INMUNOLOGICO, blank=True, null=True)
	estado_clinico = models.IntegerField(choices=ESTADO_CLINICO, blank=True, null=True)
	estadio_infeccion = models.CharField(max_length=2, blank=True, null=True)


