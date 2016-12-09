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

ORDENADOS_EN_CONSULTA = (
	(1, "SI"),
	(2, "NO"),
	(3, "N/A"),
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

TUPU_TRATAMIENTO = (
	("Isoniacida", "Isoniacida"),
	("Rifampicina", "Rifampicina"),
	("Pirazinamida", "Pirazinamida"),
	("Etambutol", "Etambutol"),
	("Estreptomicina", "Estreptomicina"),
)

STATUS_TARV = (
	(1, "Activo"),
	(2, "Abandono"),
	(3, "Reinicio"),
	(4, "Fallecido"),
	(5, "Sin Dato"),
)

#ESTA VA PARA BOLETAS
class Condiciones(models.Model):
	nombre = models.CharField(max_length=255)
	orden = models.IntegerField()
	activa = models.BooleanField(default=True)
	def __unicode__(self):
		return u'%s' % (self.nombre)

class Boletas(models.Model):
	establecimiento = models.ForeignKey(Establecimientos, blank=True, null=True)
	identidad = models.CharField(max_length=13)
	expediente = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número de Expediente Clínico o Código Identificador Único:")
	primer_nombre = models.CharField(max_length=50, blank=True, null=True, verbose_name="")
	segundo_nombre = models.CharField(max_length=50, blank=True, null=True, verbose_name="")
	primer_apellido = models.CharField(max_length=50, blank=True, null=True, verbose_name="")
	segundo_apellido = models.CharField(max_length=50, blank=True, null=True, verbose_name="")
	fecha_nacimiento = models.DateField( blank=True, null=True, verbose_name="")
	expediente = models.CharField(max_length=50, blank=True, null=True, verbose_name="Número de Expediente Clínico o Código Identificador Único:")
	sexo = models.IntegerField(choices=GENERO, verbose_name='Sexo*')
	edad_anios = models.IntegerField(verbose_name="Años")
	edad_meses = models.IntegerField(verbose_name="Meses")
	edad_dias = models.IntegerField(verbose_name="Días")
	pseudonimo = models.CharField(max_length=150, blank=True, null=True, verbose_name='Nombre Social')
	estado_civil = models.IntegerField(choices=ESTADO_CIVIL, verbose_name='Estado Civil')
	telefono_fijo = models.CharField(max_length=10, blank=True, null=True, verbose_name='Teléfono Fijo')
	telefono_celular = models.CharField(max_length=10, blank=True, null=True, verbose_name='Teléfono Celular')
	ocupacion = models.ForeignKey(Ocupaciones, null=True, blank=True)
	departamento = models.ForeignKey(Departamentos, null=True, blank=True)
	municipio = models.ForeignKey(Municipios, null=True, blank=True)
	calle = models.CharField(max_length=100, blank=True, null=True, verbose_name='Calle o Avenida')
	bloque = models.CharField(max_length=10, blank=True, null=True)
	numero_casa = models.CharField(max_length=10, blank=True, null=True, verbose_name='Número de Casa o Apartamento')
	referencias = models.CharField(max_length=500, blank=True, null=True, verbose_name='Otras Referencias')
	grupo_etnico = models.ForeignKey(GruposEtnicos, verbose_name='Grupo Étnico', blank=True, null=True)
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
	ciudad = models.ForeignKey(Ciudades, related_name='boleta_origen_ciudades', blank=True, null=True)
	barrio = models.CharField(max_length=150, blank=True, null=True, verbose_name='Barrio, Aldea, Colonia o Caserio')
	rnp = models.NullBooleanField()
	creado_por = models.ForeignKey(User, related_name='creado_por_boleta')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	actualizado_por = models.ForeignKey(User, related_name='actualizado_por_boleta')
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	condiciones = models.ManyToManyField(Condiciones, blank=True, verbose_name='Condición (marque todas las que apliquen)')
	otro_condicion = models.CharField(max_length=50, blank=True, null=True, verbose_name='Otra Condición')
	guardado = models.IntegerField(default=1)

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
	poblacion = models.IntegerField(choices=TIPO_POBLACION, verbose_name='Tipo de Población Clave Atendida')
	intervencion = models.IntegerField(choices=TIPO_INTERVENCION, verbose_name='Tipo de Intervención')
	responsable = models.CharField(max_length=100,blank=True, null=True, verbose_name='Nombre del/la Responsable de la Actividad')
	coordinador = models.CharField(max_length=100,blank=True, null=True, verbose_name='Nombre del/la Coordinador de Proyecto')
	identidad_reclutador = models.CharField(max_length=50,blank=True, null=True, verbose_name='Identidad del Reclutador')

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

class BoletasClinicas(models.Model):
	boleta = models.ForeignKey(Boletas)
	
	relaciones_mismo_sexo = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='¿Ha tenido/tiene relaciones sexuales con personas de su mismo sexo?')
	dinero_por_relaciones = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='¿Ha aceptado/acepta dinero, bienes o servicios a cambio de relaciones sexuales en los últmos meses?')
	identificacion_genero = models.IntegerField(choices=GENERO, blank=True, null=True, verbose_name='¿Cómo se identifica: Hombre o Mujer?')
	embarazada_vih = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Embarazada con VIH')
	fecha_ultima_menstruacion = models.DateField(blank=True, null=True, verbose_name='Fecha de Última Menstruación')
	semanas_gestacion = models.IntegerField(blank=True, null=True, verbose_name='Semanas de Gestación')
	evaluacion_go = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Referida por Evaluación GO')
	programacion_cesaria = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Programación por Cesária')
	fecha_cesaria = models.DateField(blank=True, null=True, verbose_name='Fecha de Eventual Cesária')
	afiliacion_seguridad_social = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Afiliación al Programa de Seguridad Social Nacional')
	clase_afiliacion =  models.CharField(max_length=200, verbose_name='Clase de Afiliación (Si Aplica)', null=True, blank=True)
	seguro_privado = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Seguro de Salud Privado')
	nombre_aseguradora = models.CharField(max_length=200, verbose_name='Nombre de la Aseguradora Social', null=True, blank=True)
	
	actualmente_tarv = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Actualmente TARV')
	fecha_inicio_tarv = models.DateField(blank=True, null=True, verbose_name='Fecha Inicio TARV')
	estatus_actual_tarv = models.IntegerField(choices=STATUS_TARV, blank=True, null=True, verbose_name='Estatus Actual')
	
	fecha_diagnostico = models.DateField(blank=True, null=True, verbose_name='Fecha del Diagnóstico de VIH')
	fecha_primera_consulta = models.DateField(blank=True, null=True, verbose_name='Fecha de 1era Consulta/Atención (Incorporación al SAI/ES)')
	fecha_proxima_cita = models.DateField(blank=True, null=True, verbose_name='Fecha de Próxima Cita')
	cita_medica = models.CharField(max_length=200, blank=True, null=True, verbose_name='Cita Médica')
	retiro_medicamento = models.CharField(max_length=200, blank=True, null=True, verbose_name='Retiro de Medicamento')
	talla = models.CharField(max_length=10, blank=True, null=True, verbose_name='Talla (Cms)')
	peso = models.CharField(max_length=10, blank=True, null=True, verbose_name='Peso (Lbs)')
	imc = models.CharField(max_length=10, blank=True, null=True, verbose_name='IMC')
	estado_inmunologico = models.IntegerField(choices=ESTADO_INMUNOLOGICO, blank=True, null=True, verbose_name='Estadio Inmunológico')
	estado_clinico = models.CharField(max_length=3, choices=ESTADIO_CLINICO, blank=True, null=True, verbose_name='Estadio Clínico')
	estadio_infeccion = models.CharField(max_length=2, blank=True, null=True, verbose_name='Estadio de la Infección')

	lic4 = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Linfocitos CD4')
	lic4_resultado = models.CharField(max_length=50, blank=True, null=True, verbose_name='Resultado (Cel./mm)')
	lic4_fecha_realizacion = models.DateField(blank=True, null=True, verbose_name='Fecha de Realización')
	lic4_ordenado_consulta = models.IntegerField(choices=ORDENADOS_EN_CONSULTA, blank=True, null=True, verbose_name='')
	caviral = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='')
	caviral_resultado = models.CharField(max_length=50, blank=True, null=True, verbose_name='Resultado (Copias/ml)')
	caviral_fecha_realizacion = models.DateField(blank=True, null=True, verbose_name='Fecha de Realización')
	caviral_ordenado_consulta = models.IntegerField(choices=ORDENADOS_EN_CONSULTA, blank=True, null=True, verbose_name='')
	hepb = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='')
	hepb_resultado = models.CharField(max_length=50, blank=True, null=True, verbose_name='Resultado')
	hepb_fecha_realizacion = models.DateField(blank=True, null=True, verbose_name='Fecha de Realización')
	hepb_ordenado_consulta = models.IntegerField(choices=ORDENADOS_EN_CONSULTA, blank=True, null=True, verbose_name='')
	hepc = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='')
	hepc_resultado = models.CharField(max_length=50, blank=True, null=True, verbose_name='Resultado')
	hepc_fecha_realizacion = models.DateField(blank=True, null=True, verbose_name='Fecha de Realización')
	hepc_ordenado_consulta = models.IntegerField(choices=ORDENADOS_EN_CONSULTA, blank=True, null=True, verbose_name='')
	rpr = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='')
	rpr_resultado = models.CharField(max_length=50, blank=True, null=True, verbose_name='Resultado')
	rpr_fecha_realizacion = models.DateField(blank=True, null=True, verbose_name='Fecha de Realización')
	rpr_ordenado_consulta = models.IntegerField(choices=ORDENADOS_EN_CONSULTA, blank=True, null=True, verbose_name='')
	rxtorax = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='')
	rxtorax_resultado = models.CharField(max_length=50, blank=True, null=True, verbose_name='Resultado')
	rxtorax_fecha_realizacion = models.DateField(blank=True, null=True, verbose_name='Fecha de Realización')
	rxtorax_ordenado_consulta = models.IntegerField(choices=ORDENADOS_EN_CONSULTA, blank=True, null=True, verbose_name='')
	sespu = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='')
	sespu_resultado = models.CharField(max_length=50, blank=True, null=True, verbose_name='Resultado')
	sespu_fecha_realizacion = models.DateField(blank=True, null=True, verbose_name='Fecha de Realización')
	sespu_ordenado_consulta = models.IntegerField(choices=ORDENADOS_EN_CONSULTA, blank=True, null=True, verbose_name='')
	ppd = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='')
	ppd_resultado = models.CharField(max_length=50, blank=True, null=True, verbose_name='Resultado')
	ppd_fecha_realizacion = models.DateField(blank=True, null=True, verbose_name='Fecha de Realización')
	ppd_ordenado_consulta = models.IntegerField(choices=ORDENADOS_EN_CONSULTA, blank=True, null=True, verbose_name='')
	cultivo = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='')
	cultivo_resultado = models.CharField(max_length=50, blank=True, null=True, verbose_name='Resultado')
	cultivo_fecha_realizacion = models.DateField(blank=True, null=True, verbose_name='Fecha de Realización')
	cultivo_ordenado_consulta = models.IntegerField(choices=ORDENADOS_EN_CONSULTA, blank=True, null=True, verbose_name='')
	usg = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='')
	usg_resultado = models.CharField(max_length=50, blank=True, null=True, verbose_name='Resultado')
	usg_fecha_realizacion = models.DateField(blank=True, null=True, verbose_name='Fecha de Realización')
	usg_ordenado_consulta = models.IntegerField(choices=ORDENADOS_EN_CONSULTA, blank=True, null=True, verbose_name='')
	biopsia = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='')
	biopsia_resultado = models.CharField(max_length=50, blank=True, null=True, verbose_name='Resultado')
	biopsia_fecha_realizacion = models.DateField(blank=True, null=True, verbose_name='Fecha de Realización')
	biopsia_ordenado_consulta = models.IntegerField(choices=ORDENADOS_EN_CONSULTA, blank=True, null=True, verbose_name='')
	otro = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='')
	otro_resultado = models.CharField(max_length=50, blank=True, null=True, verbose_name='Resultado')
	otro_fecha_realizacion = models.DateField(blank=True, null=True, verbose_name='Fecha de Realización')
	otro_ordenado_consulta = models.IntegerField(choices=ORDENADOS_EN_CONSULTA, blank=True, null=True, verbose_name='')

	tupu = models.IntegerField(choices=SI_NO, blank=True, null=True)
	tupu_diag = models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnóstico')
	tupu_initrat = models.IntegerField(choices=SI_NO, blank=True, null=True)
	tupu_fecha_initrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	tupu_entrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Actualmente en Tratamiento')
	tupu_entrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	tupu_entrat_fintrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Finalizó Tratamiento')
	tupu_entrat_fecha_fintrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	tupu_intrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Interrumpió Tratamiento')
	tupu_intrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	tupu_intrat_reitrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Reinicio Tratamiento')
	tupu_intrat_fecha_reitrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	tupu_trat = models.CharField(max_length=30,choices=TUPU_TRATAMIENTO, blank=True, null=True)

	tudi = models.IntegerField(choices=SI_NO, blank=True, null=True)
	tudi_diag = models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnóstico')
	tudi_initrat = models.IntegerField(choices=SI_NO, blank=True, null=True)
	tudi_fecha_initrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	tudi_entrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Actualmente en Tratamiento')
	tudi_entrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	tudi_entrat_fintrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Finalizó Tratamiento')
	tudi_entrat_fecha_fintrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	tudi_intrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Interrumpió Tratamiento')
	tudi_intrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	tudi_intrat_reitrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Reinicio Tratamiento')
	tudi_intrat_fecha_reitrat = models.DateField(blank=True, null=True, verbose_name='Fecha')

	hepb = models.IntegerField(choices=SI_NO, blank=True, null=True)
	hepb_diag = models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnóstico')
	hepb_initrat = models.IntegerField(choices=SI_NO, blank=True, null=True)
	hepb_fecha_initrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	hepb_entrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Actualmente en Tratamiento')
	hepb_entrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	hepb_entrat_fintrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Finalizó Tratamiento')
	hepb_entrat_fecha_fintrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	hepb_intrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Interrumpió Tratamiento')
	hepb_intrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	hepb_intrat_reitrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Reinicio Tratamiento')
	hepb_intrat_fecha_reitrat = models.DateField(blank=True, null=True, verbose_name='Fecha')


	hepc = models.IntegerField(choices=SI_NO, blank=True, null=True)
	hepc_diag = models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnóstico')
	hepc_initrat = models.IntegerField(choices=SI_NO, blank=True, null=True)
	hepc_fecha_initrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	hepc_entrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Actualmente en Tratamiento')
	hepc_entrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	hepc_entrat_fintrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Finalizó Tratamiento')
	hepc_entrat_fecha_fintrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	hepc_intrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Interrumpió Tratamiento')
	hepc_intrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	hepc_intrat_reitrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Reinicio Tratamiento')
	hepc_intrat_fecha_reitrat = models.DateField(blank=True, null=True, verbose_name='Fecha')


	ulg = models.IntegerField(choices=SI_NO, blank=True, null=True)
	ulg_diag = models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnóstico')
	ulg_initrat = models.IntegerField(choices=SI_NO, blank=True, null=True)
	ulg_fecha_initrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	ulg_entrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Actualmente en Tratamiento')
	ulg_entrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	ulg_entrat_fintrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Finalizó Tratamiento')
	ulg_entrat_fecha_fintrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	ulg_intrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Interrumpió Tratamiento')
	ulg_intrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	ulg_intrat_reitrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Reinicio Tratamiento')
	ulg_intrat_fecha_reitrat = models.DateField(blank=True, null=True, verbose_name='Fecha')


	secure = models.IntegerField(choices=SI_NO, blank=True, null=True)
	secure_diag = models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnóstico')
	secure_initrat = models.IntegerField(choices=SI_NO, blank=True, null=True)
	secure_fecha_initrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	secure_entrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Actualmente en Tratamiento')
	secure_entrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	secure_entrat_fintrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Finalizó Tratamiento')
	secure_entrat_fecha_fintrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	secure_intrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Interrumpió Tratamiento')
	secure_intrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	secure_intrat_reitrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Reinicio Tratamiento')
	secure_intrat_fecha_reitrat = models.DateField(blank=True, null=True, verbose_name='Fecha')


	fluva = models.IntegerField(choices=SI_NO, blank=True, null=True)
	fluva_diag = models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnóstico')
	fluva_initrat = models.IntegerField(choices=SI_NO, blank=True, null=True)
	fluva_fecha_initrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	fluva_entrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Actualmente en Tratamiento')
	fluva_entrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	fluva_entrat_fintrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Finalizó Tratamiento')
	fluva_entrat_fecha_fintrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	fluva_intrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Interrumpió Tratamiento')
	fluva_intrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	fluva_intrat_reitrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Reinicio Tratamiento')
	fluva_intrat_fecha_reitrat = models.DateField(blank=True, null=True, verbose_name='Fecha')

	buin = models.IntegerField(choices=SI_NO, blank=True, null=True)
	buin_diag = models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnóstico')
	buin_initrat = models.IntegerField(choices=SI_NO, blank=True, null=True)
	buin_fecha_initrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	buin_entrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Actualmente en Tratamiento')
	buin_entrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	buin_entrat_fintrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Finalizó Tratamiento')
	buin_entrat_fecha_fintrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	buin_intrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Interrumpió Tratamiento')
	buin_intrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	buin_intrat_reitrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Reinicio Tratamiento')
	buin_intrat_fecha_reitrat = models.DateField(blank=True, null=True, verbose_name='Fecha')

	edes = models.IntegerField(choices=SI_NO, blank=True, null=True)
	edes_diag = models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnóstico')
	edes_initrat = models.IntegerField(choices=SI_NO, blank=True, null=True)
	edes_fecha_initrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	edes_entrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Actualmente en Tratamiento')
	edes_entrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	edes_entrat_fintrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Finalizó Tratamiento')
	edes_entrat_fecha_fintrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	edes_intrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Interrumpió Tratamiento')
	edes_intrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	edes_intrat_reitrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Reinicio Tratamiento')
	edes_intrat_fecha_reitrat = models.DateField(blank=True, null=True, verbose_name='Fecha')


	verge = models.IntegerField(choices=SI_NO, blank=True, null=True)
	verge_diag = models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnóstico')
	verge_initrat = models.IntegerField(choices=SI_NO, blank=True, null=True)
	verge_fecha_initrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	verge_entrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Actualmente en Tratamiento')
	verge_entrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	verge_entrat_fintrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Finalizó Tratamiento')
	verge_entrat_fecha_fintrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	verge_intrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Interrumpió Tratamiento')
	verge_intrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	verge_intrat_reitrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Reinicio Tratamiento')
	verge_intrat_fecha_reitrat = models.DateField(blank=True, null=True, verbose_name='Fecha')

	trasex = models.IntegerField(choices=SI_NO, blank=True, null=True)
	trasex_diag = models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnóstico')
	trasex_initrat = models.IntegerField(choices=SI_NO, blank=True, null=True)
	trasex_fecha_initrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	trasex_entrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Actualmente en Tratamiento')
	trasex_entrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	trasex_entrat_fintrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Finalizó Tratamiento')
	trasex_entrat_fecha_fintrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	trasex_intrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Interrumpió Tratamiento')
	trasex_intrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	trasex_intrat_reitrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Reinicio Tratamiento')
	trasex_intrat_fecha_reitrat = models.DateField(blank=True, null=True, verbose_name='Fecha')

	proc = models.IntegerField(choices=SI_NO, blank=True, null=True)
	proc_diag = models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnóstico')
	proc_initrat = models.IntegerField(choices=SI_NO, blank=True, null=True)
	proc_fecha_initrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	proc_entrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Actualmente en Tratamiento')
	proc_entrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	proc_entrat_fintrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Finalizó Tratamiento')
	proc_entrat_fecha_fintrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	proc_intrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Interrumpió Tratamiento')
	proc_intrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	proc_intrat_reitrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Reinicio Tratamiento')
	proc_intrat_fecha_reitrat = models.DateField(blank=True, null=True, verbose_name='Fecha')

	infpel = models.IntegerField(choices=SI_NO, blank=True, null=True)
	infpel_diag = models.DateField(blank=True, null=True, verbose_name='Fecha de Diagnóstico')
	infpel_initrat = models.IntegerField(choices=SI_NO, blank=True, null=True)
	infpel_fecha_initrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	infpel_entrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Actualmente en Tratamiento')
	infpel_entrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	infpel_entrat_fintrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Finalizó Tratamiento')
	infpel_entrat_fecha_fintrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	infpel_intrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Interrumpió Tratamiento')
	infpel_intrat_diag = models.DateField(blank=True, null=True, verbose_name='Fecha')
	infpel_intrat_reitrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Reinicio Tratamiento')
	infpel_intrat_fecha_reitrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	
	creado_por = models.ForeignKey(User, related_name='creado_por_clinica')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	actualizado_por = models.ForeignKey(User, related_name='actualizado_por_clinica')
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return u'[%s] %s' % (self.boleta.expediente, self.boleta.identidad)

MOTIVOS_CONSULTA = {
	(1, 'Control Medico'),
	(2, 'Asistencia a Consejería/Psicología'),
	(3, 'Retiro de Medicamentos'),
	(4, 'Referido desde Otro Establecimiento'),
}

CONTEO = {
	(1, 'Menor de 200'),
	(2, 'Mayor de 200'),
}

MOTIVOS_FALLECIMIENTO = {
	(1, 'Relacionado con SIDA'),
	(2, 'Fallecimiento por TB'),
}

ESQUEMA_ARV = {
	(1, '1era Línea'),
	(2, '2da Línea'),
	(3, '3er Línea'),
}

DOCUMENTADO = {
	(1, 'Fallo Virológico'),
	(2, 'Por Fallo Clínico'),
	(3, 'Efectos Secundarios'),
	(4, 'Intolerancia a los ARV'),
	(5, 'Fallo Inmunológico'),
	(6, 'Diagnóstico de TB'),
	(7, 'Disponibilidad de ARV'),
}


class Terapias(models.Model):
	nombre = models.CharField(max_length=255)
	orden = models.IntegerField()
	def __unicode__(self):
		return u'%s' % (self.nombre)


class Medicamentos(models.Model):
	nombre = models.CharField(max_length=255)
	orden = models.IntegerField()
	def __unicode__(self):
		return u'%s' % (self.nombre)

class BoletasSeguimientos(models.Model):
	boleta_clinica = models.ForeignKey(BoletasClinicas)
	identidad = models.CharField(max_length=15)
	motivo = models.IntegerField(choices=MOTIVOS_CONSULTA, blank=True, null=True)
	profpri = models.IntegerField(choices=ORDENADOS_EN_CONSULTA, blank=True, null=True)
	fecha_consulta = models.DateField(blank=True, null=True, verbose_name='Fecha de Consulta')
	fecha_proxima_cita = models.DateField(blank=True, null=True, verbose_name='Fecha de Próxima Cita')
	
	tmpsmx = models.IntegerField(choices=SI_NO, blank=True, null=True)
	tmpsmx_initrat = models.IntegerField(choices=SI_NO, blank=True, null=True)
	tmpsmx_fecha_initrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	tmpsmx_fintrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Finalizó Tratamiento')
	tmpsmx_fecha_fintrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	tmpsmx_intrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Interrumpió Tratamiento')
	tmpsmx_fecha_intrat= models.DateField(blank=True, null=True, verbose_name='Fecha')
	tmpsmx_reitrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Reinicio Tratamiento')
	tmpsmx_fecha_reitrat = models.DateField(blank=True, null=True, verbose_name='Fecha')

	isoniacida = models.IntegerField(choices=SI_NO, blank=True, null=True)
	isoniacida_initrat = models.IntegerField(choices=SI_NO, blank=True, null=True)
	isoniacida_fecha_initrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	isoniacida_fintrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Finalizó Tratamiento')
	isoniacida_fecha_fintrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	isoniacida_intrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Interrumpió Tratamiento')
	isoniacida_fecha_intrat= models.DateField(blank=True, null=True, verbose_name='Fecha')
	isoniacida_reitrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Reinicio Tratamiento')
	isoniacida_fecha_reitrat = models.DateField(blank=True, null=True, verbose_name='Fecha')

	azitromicida = models.IntegerField(choices=SI_NO, blank=True, null=True)
	azitromicida_initrat = models.IntegerField(choices=SI_NO, blank=True, null=True)
	azitromicida_fecha_initrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	azitromicida_fintrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Finalizó Tratamiento')
	azitromicida_fecha_fintrat = models.DateField(blank=True, null=True, verbose_name='Fecha')
	azitromicida_intrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Interrumpió Tratamiento')
	azitromicida_fecha_intrat= models.DateField(blank=True, null=True, verbose_name='Fecha')
	azitromicida_reitrat = models.IntegerField(choices=SI_NO, blank=True, null=True, verbose_name='Reinicio Tratamiento')
	azitromicida_fecha_reitrat = models.DateField(blank=True, null=True, verbose_name='Fecha')

	arv_fecha_ini = models.DateField(blank=True, null=True, verbose_name='Fecha de Inicio de ARV')
	conteo_cd4 = models.IntegerField(choices=CONTEO, blank=True, null=True, verbose_name='Conteo de CD4 con que inició Terapia')
	abandono =  models.IntegerField(choices=SI_NO, blank=True, null=True)
	fecha_abandono = models.DateField(blank=True, null=True, verbose_name='Fecha de Abandono')

	suspension =  models.IntegerField(choices=SI_NO, blank=True, null=True)
	fecha_suspension = models.DateField(blank=True, null=True, verbose_name='Fecha de Suspensión')
	fecha_reinicio = models.DateField(blank=True, null=True, verbose_name='Fecha de Reinicio')

	fallecido =  models.IntegerField(choices=SI_NO, blank=True, null=True)
	fecha_fallecido = models.DateField(blank=True, null=True, verbose_name='Fecha de Fallecimiento')
	causa_fallecido =  models.IntegerField(choices=MOTIVOS_FALLECIMIENTO, blank=True, null=True)
	
	activo =  models.IntegerField(choices=SI_NO, blank=True, null=True)
	esquema_arv = models.IntegerField(choices=ESQUEMA_ARV, blank=True, null=True)
	fecha_prescripcion_arv = models.DateField(blank=True, null=True, verbose_name='Fecha de Prescripción de ARV')
	cambio_terapia =  models.IntegerField(choices=SI_NO, blank=True, null=True)
	fecha_cambio_terapia =  models.DateField(blank=True, null=True, verbose_name='Fecha de  Cambio de Terapia')
	motivo_cambio_terapia = models.IntegerField(choices=SI_NO, blank=True, null=True)
	documentado_con = models.IntegerField(choices=DOCUMENTADO, blank=True, null=True)
	esquema_actual_arv = models.IntegerField(choices=ESQUEMA_ARV, blank=True, null=True, verbose_name='Esquema Actual RV')
	fecha_entrega_arv = models.DateField(blank=True, null=True, verbose_name='Fecha de Entrega de ARV')
	
	azt = models.NullBooleanField(default=False)
	abc = models.NullBooleanField(default=False)
	efv = models.NullBooleanField(default=False)
	rpv = models.NullBooleanField(default=False)
	dtf = models.NullBooleanField(default=False)
	lpv = models.NullBooleanField(default=False)

	abc_cant = models.IntegerField(blank=True, null=True, verbose_name='Abacavir (ABC)')
	ft_cant= models.IntegerField(blank=True, null=True, verbose_name='Emtricitabina (FT)')
	d4t_cant= models.IntegerField(blank=True, null=True, verbose_name='Estavudina (D4T)')
	azt_cant = models.IntegerField(blank=True, null=True, verbose_name='Zidovunidina (AZT)')
	efv_cant= models.IntegerField(blank=True, null=True, verbose_name='Efavirenz (EFV)')
	nvp_cant= models.IntegerField(blank=True, null=True, verbose_name='Neviraparina (NVP)')
	ddi_cant= models.IntegerField(blank=True, null=True, verbose_name='Didanosida (DDI)')
	tc_cant= models.IntegerField(blank=True, null=True, verbose_name='Lamivudina (3TC)')
	tdf_cant= models.IntegerField(blank=True, null=True, verbose_name='Tenofovir (TDF)')
	rpv_cant= models.IntegerField(blank=True, null=True, verbose_name='Rilpavirina (RPV)')
	etr_cant= models.IntegerField(blank=True, null=True, verbose_name='Etravirina (ETR)')
	atv_cant= models.IntegerField(blank=True, null=True, verbose_name='Atazanavir (ATV)')
	drv_cant= models.IntegerField(blank=True, null=True, verbose_name='Darunavir (RAL)')
	fpv_cant= models.IntegerField(blank=True, null=True, verbose_name='Fosamprenavir (FPV)')
	idv_cant= models.IntegerField(blank=True, null=True, verbose_name='Indinavir (IDV)')
	nfv_cant= models.IntegerField(blank=True, null=True, verbose_name='Nelfinavir (NFV)')
	sqv_cant= models.IntegerField(blank=True, null=True, verbose_name='Saquinavir (SQV)')
	tpv_cant= models.IntegerField(blank=True, null=True, verbose_name='Tripanavir (TPV)')
	ral_cant= models.IntegerField(blank=True, null=True, verbose_name='Raltegravir (RAL)')
	evg_cant= models.IntegerField(blank=True, null=True, verbose_name='Elvitegravir (EVG)')
	dtg_cant= models.IntegerField(blank=True, null=True, verbose_name='Dolutegravir (DTG)')
	azt_3tc_cant= models.IntegerField(blank=True, null=True, verbose_name='AZT_3TC')
	abc_3tc_azt_cant= models.IntegerField(blank=True, null=True, verbose_name='ACB_3TC_AZT')
	efv_ftc_tdf_cant= models.IntegerField(blank=True, null=True, verbose_name='EFV_FTC_TDF')
	rpv_ftc_tdf_cant= models.IntegerField(blank=True, null=True, verbose_name='RPV_FTC_TDF')
	tdf_ftc_cant= models.IntegerField(blank=True, null=True, verbose_name='TDF_FTC')
	lpv_rtv_cant= models.IntegerField(blank=True, null=True, verbose_name='LPV_rtv')
	abc_3tc_cant= models.IntegerField(blank=True, null=True, verbose_name='ABC_3TC')

	abc_med = models.NullBooleanField(default=False)
	ft_med= models.NullBooleanField(default=False)
	d4t_med= models.NullBooleanField(default=False)
	azt_med = models.NullBooleanField(default=False)
	efv_med= models.NullBooleanField(default=False)
	nvp_med= models.NullBooleanField(default=False)
	ddi_med= models.NullBooleanField(default=False)
	tc_med= models.NullBooleanField(default=False)
	tdf_med= models.NullBooleanField(default=False)
	rpv_med= models.NullBooleanField(default=False)
	etr_med= models.NullBooleanField(default=False)
	atv_med= models.NullBooleanField(default=False)
	drv_med= models.NullBooleanField(default=False)
	fpv_med= models.NullBooleanField(default=False)
	idv_med= models.NullBooleanField(default=False)
	nfv_med= models.NullBooleanField(default=False)
	sqv_med= models.NullBooleanField(default=False)
	tpv_med= models.NullBooleanField(default=False)
	ral_med= models.NullBooleanField(default=False)
	evg_med= models.NullBooleanField(default=False)
	dtg_med= models.NullBooleanField(default=False)

	abc_ter = models.NullBooleanField(default=False)
	ft_ter= models.NullBooleanField(default=False)
	d4t_ter= models.NullBooleanField(default=False)
	azt_ter = models.NullBooleanField(default=False)
	efv_ter= models.NullBooleanField(default=False)
	nvp_ter= models.NullBooleanField(default=False)
	ddi_ter= models.NullBooleanField(default=False)
	tc_ter= models.NullBooleanField(default=False)
	tdf_ter= models.NullBooleanField(default=False)
	rpv_ter= models.NullBooleanField(default=False)
	etr_ter= models.NullBooleanField(default=False)
	atv_ter= models.NullBooleanField(default=False)
	drv_ter= models.NullBooleanField(default=False)
	fpv_ter= models.NullBooleanField(default=False)
	idv_ter= models.NullBooleanField(default=False)
	nfv_ter= models.NullBooleanField(default=False)
	sqv_ter= models.NullBooleanField(default=False)
	tpv_ter= models.NullBooleanField(default=False)
	ral_ter= models.NullBooleanField(default=False)
	evg_ter= models.NullBooleanField(default=False)
	dtg_ter= models.NullBooleanField(default=False)

	azt2_ter = models.NullBooleanField(default=False)
	abc2_ter = models.NullBooleanField(default=False)
	efv2_ter = models.NullBooleanField(default=False)
	rpv2_ter = models.NullBooleanField(default=False)
	dtf2_ter = models.NullBooleanField(default=False)
	lpv2_ter = models.NullBooleanField(default=False)

		

	cantidad_medicamento =  models.IntegerField(blank=True, null=True, verbose_name='Cantidad de Medicamento Contados')
	adherencia = models.IntegerField(blank=True, null=True, verbose_name='Porcentaje de Adherencia')
	tiempo_arv = models.IntegerField(blank=True, null=True, verbose_name='Tiempo enn ARV')
	fecha_proxentrega_arv = models.DateField(blank=True, null=True, verbose_name='Fecha de Próxima Entrega de ARV')

	creado_por = models.ForeignKey(User, related_name='creado_por_seguimiento')
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	actualizado_por = models.ForeignKey(User, related_name='actualizado_por_seguimiento')
	fecha_actualizacion = models.DateTimeField(auto_now=True)
	
	def __unicode__(self):
		return u'[%s] %s' % (self.boleta_clinica.boleta.expediente, self.boleta_clinica.boleta.identidad)