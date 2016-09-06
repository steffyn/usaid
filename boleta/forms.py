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
		widgets = {
			'lic4_resultado': TextInput(attrs={'type': 'number'}),
			'caviral_resultado': TextInput(attrs={'type': 'number'}),
			'rxtorax_resultado': TextInput(attrs={'type': 'number'}),
		}
		fields = "__all__"
		exclude = ['hepb_resultado','rpr_resultado','hepc_resultado','estado_clinico','embarazada_vih','evaluacion_go','programacion_cesaria','afiliacion_seguridad_social','seguro_privado','relaciones_mismo_sexo','dinero_por_relaciones','identificacion_genero','lic4','lic4_ordenado_consulta','caviral','caviral_ordenado_consulta','hepb','hepb_ordenado_consulta','hepc','hepc_ordenado_consulta','rpr','rpr_ordenado_consulta','rxtorax','rxtorax_ordenado_consulta','sespu','sespu_ordenado_consulta','ppd','ppd_ordenado_consulta','cultivo','cultivo_ordenado_consulta','usg','usg_ordenado_consulta','biopsia','biopsia_ordenado_consulta','otro','otro_ordenado_consulta','tupu','tupu_initrat','tupu_entrat','tupu_entrat_fintrat','tupu_intrat','tupu_intrat_reitrat','tupu_trat','tudi','tudi_initrat','tudi_entrat','tudi_entrat_fintrat','tudi_intrat','tudi_intrat_reitrat','tudi_trat','hepb','hepb_initrat','hepb_entrat','hepb_entrat_fintrat','hepb_intrat','hepb_intrat_reitrat','hepb_trat','hepc','hepc_initrat','hepc_entrat','hepc_entrat_fintrat','hepc_intrat','hepc_intrat_reitrat','hepc_trat','ulg','ulg_initrat','ulg_entrat','ulg_entrat_fintrat','ulg_intrat','ulg_intrat_reitrat','ulg_trat','secure','secure_initrat','secure_entrat','secure_entrat_fintrat','secure_intrat','secure_intrat_reitrat','secure_trat','fluva','fluva_initrat','fluva_entrat','fluva_entrat_fintrat','fluva_intrat','fluva_intrat_reitrat','fluva_trat','buin','buin_initrat','buin_entrat','buin_entrat_fintrat','buin_intrat','buin_intrat_reitrat','buin_trat','edes','edes_initrat','edes_entrat','edes_entrat_fintrat','edes_intrat','edes_intrat_reitrat','edes_trat','verge','verge_initrat','verge_entrat','verge_entrat_fintrat','verge_intrat','verge_intrat_reitrat','verge_trat','trasex','trasex_initrat','trasex_entrat','trasex_entrat_fintrat','trasex_intrat','trasex_intrat_reitrat','trasex_trat','proc','proc_initrat','proc_entrat','proc_entrat_fintrat','proc_intrat','proc_intrat_reitrat','proc_trat','infpel','infpel_initrat','infpel_entrat','infpel_entrat_fintrat','infpel_intrat','infpel_intrat_reitrat','infpel_tra','actualizado_por', 'creado_por', 'fecha_creacion', 'fecha_actualizacion', 'boleta', 'establecimiento']
	
	estado_inmunologico =  forms.ChoiceField(widget=RadioSelect, choices=ESTADO_INMUNOLOGICO, label='Estadio Inmunologico', required=False, initial=None)
	estado_clinico =  forms.ChoiceField(widget=RadioSelect, choices=ESTADIO_CLINICO, label='Estadio Clinico', required=False, initial=None)
	embarazada_vih =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Embarazada con VIH', required=False, initial=None)
	evaluacion_go =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Referida por Evaluación GO', required=False, initial=None)
	programacion_cesaria =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Programación por Cesária', required=False, initial=None)
	afiliacion_seguridad_social =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Afiliación al Programa de Seguridad Social Nacional', required=False, initial=None)
	seguro_privado =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Seguro de Salud Privado', required=False, initial=None)
	relaciones_mismo_sexo =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='¿Ha tenido/tiene relaciones sexuales con personas de su mismo sexo?', required=False, initial=None)
	dinero_por_relaciones =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='¿Ha aceptado/acepta dinero, bienes o servicios a cambio de relaciones sexuales en los últmos meses?', required=False, initial=None)
	identificacion_genero =  forms.ChoiceField(widget=RadioSelect, choices=GENERO, label='¿Cómo se identifica: Hombre o Mujer?', required=False, initial=None)
	
	hepb_resultado =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Resultado', required=False, initial=None)
	hepc_resultado =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Resultado', required=False, initial=None)
	rpr_resultado =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Resultado', required=False, initial=None)

	lic4 =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Linfocitos C4', required=False, initial=None)
	lic4_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False, initial=None)
	caviral =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Carga Viral', required=False, initial=None)
	caviral_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False, initial=None)
	hepb =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Virus de Hepatitis B', required=False, initial=None)
	hepb_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False, initial=None)
	hepc =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Virus de Hepatitis C', required=False, initial=None)
	hepc_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False, initial=None)
	rpr =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='RPR (Sifilis) / VDRL', required=False, initial=None)
	rpr_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False, initial=None)
	rxtorax =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='RX Torax', required=False, initial=None)
	rxtorax_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False, initial=None)
	sespu =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Seriado de Esputo', required=False, initial=None)
	sespu_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False, initial=None)
	ppd =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='PPD', required=False, initial=None)
	ppd_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False, initial=None)
	cultivo =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Cultivo', required=False, initial=None)
	cultivo_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False, initial=None)
	usg =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='USG', required=False, initial=None)
	usg_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False, initial=None)
	biopsia =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Biopsia', required=False, initial=None)
	biopsia_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False, initial=None)
	otro =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Otro', required=False, initial=None)
	otro_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False, initial=None)
	tupu =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='TUBERCULOSIS PULMUNAR', required=False, initial=None)
	tupu_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False, initial=None)
	tupu_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False, initial=None)
	tupu_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False, initial=None)
	tupu_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False, initial=None)
	tupu_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False, initial=None)
	tupu_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False, initial=None)
	tudi =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='TUBERCULOSIS DETERMINADA O EXTRA PULMONAR', required=False, initial=None)
	tudi_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False, initial=None)
	tudi_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False, initial=None)
	tudi_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False, initial=None)
	tudi_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False, initial=None)
	tudi_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False, initial=None)
	tudi_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False, initial=None)
	hepb =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='HEPATITIS B', required=False, initial=None)
	hepb_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False, initial=None)
	hepb_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False, initial=None)
	hepb_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False, initial=None)
	hepb_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False, initial=None)
	hepb_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False, initial=None)
	hepb_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False, initial=None)
	hepc =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='HEPATITIS C', required=False, initial=None)
	hepc_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False, initial=None)
	hepc_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False, initial=None)
	hepc_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False, initial=None)
	hepc_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False, initial=None)
	hepc_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False, initial=None)
	hepc_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False, initial=None)
	ulg =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='SINDROME DE ULCERA GENITAL', required=False, initial=None)
	ulg_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False, initial=None)
	ulg_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False, initial=None)
	ulg_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False, initial=None)
	ulg_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False, initial=None)
	ulg_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False, initial=None)
	ulg_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False, initial=None)
	secure =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='SINDROME SECRESION URETAL', required=False, initial=None)
	secure_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False, initial=None)
	secure_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False, initial=None)
	secure_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False, initial=None)
	secure_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False, initial=None)
	secure_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False, initial=None)
	secure_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False, initial=None)
	fluva =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='SINDROME FLUJO VAGINAL', required=False, initial=None)
	fluva_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False, initial=None)
	fluva_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False, initial=None)
	fluva_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False, initial=None)
	fluva_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False, initial=None)
	fluva_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False, initial=None)
	fluva_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False, initial=None)
	buin =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='SINDROME BUBON INGUINAL', required=False, initial=None)
	buin_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False, initial=None)
	buin_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False, initial=None)
	buin_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False, initial=None)
	buin_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False, initial=None)
	buin_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False, initial=None)
	buin_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False, initial=None)
	edes =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='SINDROME EDEMA DE ESCROTO', required=False, initial=None)
	edes_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False, initial=None)
	edes_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False, initial=None)
	edes_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False, initial=None)
	edes_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False, initial=None)
	edes_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False, initial=None)
	edes_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False, initial=None)
	verge =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='SINDROME DE VERRUGAS GENITALES', required=False, initial=None)
	verge_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False, initial=None)
	verge_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False, initial=None)
	verge_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False, initial=None)
	verge_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False, initial=None)
	verge_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False, initial=None)
	verge_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False, initial=None)
	trasex =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='FARINGITIS DE TRANSMISION SEXUAL', required=False, initial=None)
	trasex_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False, initial=None)
	trasex_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False, initial=None)
	trasex_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False, initial=None)
	trasex_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False, initial=None)
	trasex_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False, initial=None)
	trasex_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False, initial=None)
	proc =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='PROCITITIS, PROCTOCOLITIS, ENTERITIS', required=False, initial=None)
	proc_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False, initial=None)
	proc_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False, initial=None)
	proc_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False, initial=None)
	proc_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False, initial=None)
	proc_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False, initial=None)
	proc_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False, initial=None)
	infpel =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='ENFERMEDAD INFLAMATORIA PELVICA', required=False, initial=None)
	infpel_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False, initial=None)
	infpel_entrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente en Tratamiento', required=False, initial=None)
	infpel_entrat_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False, initial=None)
	infpel_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpio Tratamiento', required=False, initial=None)
	infpel_intrat_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinicio Tratamiento', required=False, initial=None)
	infpel_trat =  forms.ChoiceField(widget=RadioSelect, choices=TUPU_TRATAMIENTO, label='Tratamiento', required=False, initial=None)






