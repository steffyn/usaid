# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.forms.widgets import *
from django import forms
from boleta.models import *
from general.models import *
from django.contrib.auth.models import User

from django.utils.safestring import mark_safe

ESTADO_CIVIL = (
	(1, "Soltero(a)"),
	(2, "Casado(a)"),
	(3, "Union Libre"),
)

RESULTADOS = (
	(1, "Positivo"),
	(2, "Negativo"),
)

TIPO_POBLACION = (
	(1, "MTS"),
	(2, "HSH/TG"),
)

SI_NO = (
	(1, "Si"),
	(2, "No"),
)

ORDENADOS_EN_CONSULTA = (
	(1, "SI"),
	(2, "NO"),
	(3, "N/A"),
)

TUPU_TRATAMIENTO = (
	("Isoniacida", "Isoniacida"),
	("Rifampicina", "Rifampicina"),
	("Pirazinamida", "Pirazinamida"),
	("Etambutol", "Etambutol"),
	("Estreptomicina", "Estreptomicina"),
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

GENERO = (
	(1, "Hombre"),
	(2, "Mujer"),
)

class BoletaForm(ModelForm):
	class Meta:
		model = Boletas
		fields = "__all__"
		exclude = ['actualizado_por', 'creado_por', 'identidad', 'expediente', 'sexo', 'municipio', 'ciudad', 'barrio',
					'primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'fecha_nacimiento']
		widgets = {
			'edad_anios': TextInput(attrs={'readonly': 'readonly', 'type': 'text'}),
			'edad_meses': TextInput(attrs={'readonly': 'readonly', 'type': 'text'}),
		}
	poblacion =  forms.ModelChoiceField(queryset=Poblaciones.objects.all(), widget=RadioSelect, empty_label=None )
	grupo_etnico =  forms.ModelChoiceField(queryset=GruposEtnicos.objects.all(), widget=RadioSelect, empty_label=None )
	estado_civil =  forms.ChoiceField(choices=ESTADO_CIVIL, widget=RadioSelect)
	
class BoletaConsejeriaForm(ModelForm):
	class Meta:
		model = BoletasConsejeria
		fields = "__all__"
		exclude = ['actualizado_por', 'nombre_persona_solicitante', 'nombre_consejero', 'creado_por', 'fecha_creacion', 'fecha_actualizacion', 'boleta']
		widgets = {
			'periodicidad': TextInput(attrs={'readonly': 'readonly', 'type': 'text', 'value': '1'}),
		}

class BoletasConsejeriaPostPruebaForm(ModelForm):
	class Meta:
		model = BoletasConsejeriaPostPrueba
		fields = "__all__"
		exclude = ['actualizado_por', 'nombre_persona_solicitante', 'nombre_consejero', 'creado_por', 'fecha_creacion', 'fecha_actualizacion', 'boleta']
		widgets = {
			'observaciones' : Textarea()
		}

class BoletaPruebaForm(ModelForm):
	class Meta:
		model = BoletasPruebas
		widgets = {
			'numero_prueba': TextInput(attrs={'readonly': 'readonly'}),
			'nombre_persona_prueba': TextInput(attrs={'readonly': 'readonly'}),
		}
		fields = "__all__"
		exclude = ['actualizado_por', 'nombre_persona_solicitante', 'nombre_consejero', 'creado_por', 'fecha_creacion', 'fecha_actualizacion', 'boleta']
	resultado_prueba_tamizaje =  forms.ChoiceField(choices=RESULTADOS, widget=RadioSelect)
	resultado_prueba_confirmatoria =  forms.ChoiceField(choices=RESULTADOS, widget=RadioSelect)


class AsistenciaForm(ModelForm):
	class Meta:
		model = Asistencia
		fields = "__all__"
		exclude = ['actualizado_por', 'creado_por', 'fecha_creacion', 'fecha_actualizacion']
	poblacion =  forms.ChoiceField(choices=TIPO_POBLACION, widget=RadioSelect)

class BoletaClinicaForm(ModelForm):
	class Meta:
		model = BoletasClinicas
		fields = "__all__"
		exclude = ['actualizado_por', 'creado_por', 'fecha_creacion', 'fecha_actualizacion', 'boleta', 'establecimiento']
	estado_inmunologico =  forms.ChoiceField(widget=RadioSelect, choices=ESTADO_INMUNOLOGICO, label='Estadio Inmunologico', required=False)
	estado_clinico =  forms.ChoiceField(widget=RadioSelect, choices=ESTADIO_CLINICO, label='Estadio Clinico', required=False)
	embarazada_vih =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Embarazada con VIH', required=False)
	evaluacion_go =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Referida por Evaluación GO', required=False)
	programacion_cesaria =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Programación por Cesária', required=False)
	afiliacion_seguridad_social =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Afiliación al Programa de Seguridad Social Nacional', required=False)
	seguro_privado =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Seguro de Salud Privado', required=False)
	relaciones_mismo_sexo =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='¿Ha tenido/tiene relaciones sexuales con personas de su mismo sexo?', required=False)
	dinero_por_relaciones =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='¿Ha aceptado/acepta dinero, bienes o servicios a cambio de relaciones sexuales en los últmos meses?', required=False)
	identificacion_genero =  forms.ChoiceField(widget=RadioSelect, choices=GENERO, label='¿Cómo se identifica: Hombre o Mujer?', required=False)
	lic4 =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Linfocitos C4', required=False)
	lic4_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False)
	caviral =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Carga Viral', required=False)
	caviral_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False)
	hepb =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Virus de Hepatitis B', required=False)
	hepb_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False)
	hepc =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Virus de Hepatitis C', required=False)
	hepc_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False)
	rpr =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='RPR (Sifilis) / VDRL', required=False)
	rpr_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False)
	rxtorax =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='RX Torax', required=False)
	rxtorax_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False)
	sespu =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Seriado de Esputo', required=False)
	sespu_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False)
	ppd =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='PPD', required=False)
	ppd_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False)
	cultivo =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Cultivo', required=False)
	cultivo_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False)
	usg =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='USG', required=False)
	usg_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False)
	biopsia =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Biopsia', required=False)
	biopsia_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False)
	otro =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Otro', required=False)
	otro_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False)
	tupu =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='TUBERCULOSIS PULMUNAR', required=False)
	tupu_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False)
	tupu_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False)
	tupu_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False)
	tupu_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False)
	tupu_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False)
	tupu_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False)
	tudi =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='TUBERCULOSIS DETERMINADA O EXTRA PULMONAR', required=False)
	tudi_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False)
	tudi_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False)
	tudi_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False)
	tudi_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False)
	tudi_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False)
	tudi_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False)
	hepb =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='HEPATITIS B', required=False)
	hepb_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False)
	hepb_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False)
	hepb_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False)
	hepb_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False)
	hepb_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False)
	hepb_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False)
	hepc =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='HEPATITIS C', required=False)
	hepc_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False)
	hepc_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False)
	hepc_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False)
	hepc_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False)
	hepc_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False)
	hepc_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False)
	ulg =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='SINDROME DE ULCERA GENITAL', required=False)
	ulg_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False)
	ulg_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False)
	ulg_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False)
	ulg_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False)
	ulg_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False)
	ulg_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False)
	secure =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='SINDROME SECRESION URETAL', required=False)
	secure_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False)
	secure_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False)
	secure_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False)
	secure_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False)
	secure_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False)
	secure_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False)
	fluva =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='SINDROME FLUJO VAGINAL', required=False)
	fluva_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False)
	fluva_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False)
	fluva_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False)
	fluva_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False)
	fluva_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False)
	fluva_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False)
	buin =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='SINDROME BUBON INGUINAL', required=False)
	buin_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False)
	buin_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False)
	buin_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False)
	buin_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False)
	buin_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False)
	buin_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False)
	edes =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='SINDROME EDEMA DE ESCROTO', required=False)
	edes_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False)
	edes_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False)
	edes_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False)
	edes_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False)
	edes_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False)
	edes_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False)
	verge =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='SINDROME DE VERRUGAS GENITALES', required=False)
	verge_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False)
	verge_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False)
	verge_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False)
	verge_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False)
	verge_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False)
	verge_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False)
	trasex =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='FARINGITIS DE TRANSMISION SEXUAL', required=False)
	trasex_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False)
	trasex_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False)
	trasex_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False)
	trasex_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False)
	trasex_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False)
	trasex_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False)
	proc =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='PROCITITIS, PROCTOCOLITIS, ENTERITIS', required=False)
	proc_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False)
	proc_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False)
	proc_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False)
	proc_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False)
	proc_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False)
	proc_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False)
	infpel =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='ENFERMEDAD INFLAMATORIA PELVICA', required=False)
	infpel_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False)
	infpel_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False)
	infpel_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False)
	infpel_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False)
	infpel_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False)
	infpel_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False)






