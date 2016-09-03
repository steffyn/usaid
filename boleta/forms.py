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
		exclude = ['actualizado_por', 'creado_por', 'fecha_creacion', 'fecha_actualizacion', 'boleta']

	estado_inmunologico =  forms.ChoiceField(widget=RadioSelect, choices=ESTADO_INMUNOLOGICO, label='Estadio Inmunologico')
	estado_clinico =  forms.ChoiceField(widget=RadioSelect, choices=ESTADIO_CLINICO, label='Estadio Clinico')
	embarazada_vih =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Embarazada con VIH')
	evaluacion_go =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Referida por Evaluación GO')
	programacion_cesaria =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Programación por Cesária')
	afiliacion_seguridad_social =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Afiliación al Programa de Seguridad Social Nacional')
	seguro_privado =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Seguro de Salud Privado')
	relaciones_mismo_sexo =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='¿Ha tenido/tiene relaciones sexuales con personas de su mismo sexo?')
	dinero_por_relaciones =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='¿Ha aceptado/acepta dinero, bienes o servicios a cambio de relaciones sexuales en los últmos meses?')
	identificacion_genero =  forms.ChoiceField(widget=RadioSelect, choices=GENERO, label='¿Cómo se identifica: Hombre o Mujer?')
	
	lic4 =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Linfocitos C4')
	lic4_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta')
	caviral =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Carga Viral')
	caviral_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta')
	hepb =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Virus de Hepatitis B')
	hepb_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta')
	hepc =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Virus de Hepatitis C')
	hepc_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta')
	rpr =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='RPR (Sifilis) / VDRL')
	rpr_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta')
	rxtorax =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='RX Torax')
	rxtorax_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta')
	sespu =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Seriado de Esputo')
	sespu_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta')
	ppd =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='PPD')
	ppd_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta')
	cultivo =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Cultivo')
	cultivo_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta')
	usg =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='USG')
	usg_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta')
	biopsia =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Biopsia')
	biopsia_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta')
	otro =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Otro')
	otro_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta')


	tupu =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='TUBERCULOSIS PULMUNAR')
	tupu_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento')
	tupu_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento')
	tupu_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento')
	tupu_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento')
	tupu_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento')
	tupu_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento')
	
	tudi =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='TUBERCULOSIS DETERMINADA O EXTRA PULMONAR')
	tudi_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento')
	tudi_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento')
	tudi_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento')
	tudi_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento')
	tudi_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento')
	tudi_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento')


	hepb =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='HEPATITIS B')
	hepb_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento')
	hepb_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento')
	hepb_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento')
	hepb_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento')
	hepb_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento')
	hepb_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento')


	hepc =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='HEPATITIS C')
	hepc_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento')
	hepc_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento')
	hepc_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento')
	hepc_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento')
	hepc_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento')
	hepc_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento')


	ulg =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='SINDROME DE ULCERA GENITAL')
	ulg_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento')
	ulg_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento')
	ulg_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento')
	ulg_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento')
	ulg_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento')
	ulg_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento')


	secure =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='SINDROME SECRESION URETAL')
	secure_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento')
	secure_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento')
	secure_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento')
	secure_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento')
	secure_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento')
	secure_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento')


	fluva =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='SINDROME FLUJO VAGINAL')
	fluva_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento')
	fluva_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento')
	fluva_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento')
	fluva_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento')
	fluva_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento')
	fluva_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento')


	buin =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='SINDROME BUBON INGUINAL')
	buin_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento')
	buin_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento')
	buin_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento')
	buin_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento')
	buin_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento')
	buin_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento')


	edes =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='SINDROME EDEMA DE ESCROTO')
	edes_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento')
	edes_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento')
	edes_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento')
	edes_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento')
	edes_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento')
	edes_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento')


	verge =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='SINDROME DE VERRUGAS GENITALES')
	verge_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento')
	verge_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento')
	verge_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento')
	verge_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento')
	verge_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento')
	verge_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento')


	trasex =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='FARINGITIS DE TRANSMISION SEXUAL')
	trasex_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento')
	trasex_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento')
	trasex_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento')
	trasex_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento')
	trasex_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento')
	trasex_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento')

	proc =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='PROCITITIS, PROCTOCOLITIS, ENTERITIS')
	proc_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento')
	proc_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento')
	proc_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento')
	proc_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento')
	proc_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento')
	proc_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento')

	infpel =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='ENFERMEDAD INFLAMATORIA PELVICA')
	infpel_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento')
	infpel_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento')
	infpel_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento')
	infpel_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento')
	infpel_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento')
	infpel_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento')






