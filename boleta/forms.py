# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.forms.widgets import *
from django import forms
from boleta.models import *
from general.models import *
from django.contrib.auth.models import User

from django.utils.safestring import mark_safe
from geelweb.django.twitter_bootstrap_form.widgets import TextInputWithButton
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


STATUS_TARV = (
	(1, "Activo"),
	(2, "Abandono"),
	(3, "Reinicio"),
	(4, "Fallecido"),
	(5, "Sin Dato"),
)

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

class BoletaForm(ModelForm):
	class Meta:
		model = Boletas
		fields = "__all__"
		exclude = ['guardado','actualizado_por', 'creado_por', 'identidad', 'expediente', 'sexo', 'municipio', 'ciudad',
					'primer_nombre', 'segundo_nombre', 'establecimiento' 'primer_apellido', 'segundo_apellido', 'fecha_nacimiento']
		widgets = {
			'edad_anios': TextInput(attrs={'readonly': 'readonly', 'type': 'text'}),
			'edad_meses': TextInput(attrs={'readonly': 'readonly', 'type': 'text'}),
			'edad_dias': TextInput(attrs={'readonly': 'readonly', 'type': 'text'}),
		}
	poblacion =  forms.ModelChoiceField(queryset=Poblaciones.objects.all(), widget=RadioSelect, empty_label=None,  required=False)
	grupo_etnico =  forms.ModelChoiceField(queryset=GruposEtnicos.objects.all(), widget=RadioSelect, empty_label=None,  required=False)
	estado_civil =  forms.ChoiceField(choices=ESTADO_CIVIL, widget=RadioSelect, label='Estado Civil*')
	
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
			'lic4_resultado': TextInput(attrs={'type': 'number', 'step':'00.01'}),
			'caviral_resultado': TextInput(attrs={'type': 'number', 'step':'00.01'}),
			'rxtorax_resultado': TextInput(attrs={'type': 'number'}),
		}
		fields = "__all__"
		exclude = ['hepb_resultado','rpr_resultado','hepc_resultado','estado_clinico','embarazada_vih','evaluacion_go','programacion_cesaria','afiliacion_seguridad_social','seguro_privado','relaciones_mismo_sexo','dinero_por_relaciones','identificacion_genero','lic4','lic4_ordenado_consulta','caviral','caviral_ordenado_consulta','hepb','hepb_ordenado_consulta','hepc','hepc_ordenado_consulta','rpr','rpr_ordenado_consulta','rxtorax','rxtorax_ordenado_consulta','sespu','sespu_ordenado_consulta','ppd','ppd_ordenado_consulta','cultivo','cultivo_ordenado_consulta','usg','usg_ordenado_consulta','biopsia','biopsia_ordenado_consulta','otro','otro_ordenado_consulta','tupu','tupu_initrat','tupu_entrat','tupu_entrat_fintrat','tupu_intrat','tupu_intrat_reitrat','tupu_trat','tudi','tudi_initrat','tudi_entrat','tudi_entrat_fintrat','tudi_intrat','tudi_intrat_reitrat','tudi_trat','hepb','hepb_initrat','hepb_entrat','hepb_entrat_fintrat','hepb_intrat','hepb_intrat_reitrat','hepb_trat','hepc','hepc_initrat','hepc_entrat','hepc_entrat_fintrat','hepc_intrat','hepc_intrat_reitrat','hepc_trat','ulg','ulg_initrat','ulg_entrat','ulg_entrat_fintrat','ulg_intrat','ulg_intrat_reitrat','ulg_trat','secure','secure_initrat','secure_entrat','secure_entrat_fintrat','secure_intrat','secure_intrat_reitrat','secure_trat','fluva','fluva_initrat','fluva_entrat','fluva_entrat_fintrat','fluva_intrat','fluva_intrat_reitrat','fluva_trat','buin','buin_initrat','buin_entrat','buin_entrat_fintrat','buin_intrat','buin_intrat_reitrat','buin_trat','edes','edes_initrat','edes_entrat','edes_entrat_fintrat','edes_intrat','edes_intrat_reitrat','edes_trat','verge','verge_initrat','verge_entrat','verge_entrat_fintrat','verge_intrat','verge_intrat_reitrat','verge_trat','trasex','trasex_initrat','trasex_entrat','trasex_entrat_fintrat','trasex_intrat','trasex_intrat_reitrat','trasex_trat','proc','proc_initrat','proc_entrat','proc_entrat_fintrat','proc_intrat','proc_intrat_reitrat','proc_trat','infpel','infpel_initrat','infpel_entrat','infpel_entrat_fintrat','infpel_intrat','infpel_intrat_reitrat','infpel_tra','actualizado_por', 'creado_por', 'fecha_creacion', 'fecha_actualizacion', 'boleta', 'establecimiento',
					'fecha_ultima_menstruacion','fecha_cesaria','fecha_inicio_tarv','fecha_diagnostico','fecha_primera_consulta','fecha_proxima_cita','lic4_fecha_realizacion','caviral_fecha_realizacion','hepb_fecha_realizacion','hepc_fecha_realizacion','rpr_fecha_realizacion','rxtorax_fecha_realizacion','sespu_fecha_realizacion','ppd_fecha_realizacion','cultivo_fecha_realizacion','usg_fecha_realizacion','biopsia_fecha_realizacion','otro_fecha_realizacion','tupu_diag','tupu_fecha_initrat','tupu_entrat_diag','tupu_entrat_fecha_fintrat','tupu_intrat_diag','tupu_intrat_fecha_reitrat','tudi_diag','tudi_fecha_initrat','tudi_entrat_diag','tudi_entrat_fecha_fintrat','tudi_intrat_diag','tudi_intrat_fecha_reitrat','hepb_diag','hepb_fecha_initrat','hepb_entrat_diag','hepb_entrat_fecha_fintrat','hepb_intrat_diag','hepb_intrat_fecha_reitrat','hepc_diag','hepc_fecha_initrat','hepc_entrat_diag','hepc_entrat_fecha_fintrat','hepc_intrat_diag','hepc_intrat_fecha_reitrat','ulg_diag','ulg_fecha_initrat','ulg_entrat_diag','ulg_entrat_fecha_fintrat','ulg_intrat_diag','ulg_intrat_fecha_reitrat','secure_diag','secure_fecha_initrat','secure_entrat_diag','secure_entrat_fecha_fintrat','secure_intrat_diag','secure_intrat_fecha_reitrat','fluva_diag','fluva_fecha_initrat','fluva_entrat_diag','fluva_entrat_fecha_fintrat','fluva_intrat_diag','fluva_intrat_fecha_reitrat','buin_diag','buin_fecha_initrat','buin_entrat_diag','buin_entrat_fecha_fintrat','buin_intrat_diag','buin_intrat_fecha_reitrat','edes_diag','edes_fecha_initrat','edes_entrat_diag','edes_entrat_fecha_fintrat','edes_intrat_diag','edes_intrat_fecha_reitrat','verge_diag','verge_fecha_initrat','verge_entrat_diag','verge_entrat_fecha_fintrat','verge_intrat_diag','verge_intrat_fecha_reitrat','trasex_diag','trasex_fecha_initrat','trasex_entrat_diag','trasex_entrat_fecha_fintrat','trasex_intrat_diag','trasex_intrat_fecha_reitrat','proc_diag','proc_fecha_initrat','proc_entrat_diag','proc_entrat_fecha_fintrat','proc_intrat_diag','proc_intrat_fecha_reitrat','infpel_diag','infpel_fecha_initrat','infpel_entrat_diag','infpel_entrat_fecha_fintrat','infpel_intrat_diag','infpel_intrat_fecha_reitrat',
		]
	
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
	
	hepb_resultado =  forms.ChoiceField(widget=RadioSelect, choices=RESULTADOS, label='Resultado', required=False, initial=None)
	hepc_resultado =  forms.ChoiceField(widget=RadioSelect, choices=RESULTADOS, label='Resultado', required=False, initial=None)
	rpr_resultado =  forms.ChoiceField(widget=RadioSelect, choices=RESULTADOS, label='Resultado', required=False, initial=None)
	
	actualmente_tarv =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente TARV', required=False, initial=None)
	estatus_actual_tarv =  forms.ChoiceField(widget=RadioSelect, choices=STATUS_TARV, label='', required=False, initial=None)

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
	usg =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='USG(Ultrasograma)', required=False, initial=None)
	usg_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False, initial=None)
	biopsia =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Biopsia', required=False, initial=None)
	biopsia_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False, initial=None)
	otro =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Otro', required=False, initial=None)
	otro_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False, initial=None)
	tupu =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='TUBERCULOSIS PULMONAR', required=False, initial=None)
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
	secure =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='SINDROME SECRECION URETAL', required=False, initial=None)
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


	fecha_inicio_tarv = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fecha_inicio_tarv',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha Inicio TARV')

	fecha_ultima_menstruacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fecha_ultima_menstruacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Última Menstruación')

	fecha_cesaria = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fecha_cesaria',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Eventual Cesária')

	fecha_diagnostico = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fecha_diagnostico',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha del Diagnóstico de VIH')

	fecha_primera_consulta = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fecha_primera_consulta',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de 1era Consulta/Atención (Incorporación al SAI/ES)')

	fecha_proxima_cita = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fecha_proxima_cita',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Próxima Cita')

	lic4_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_lic4_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	hepb_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepb_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	hepc_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepc_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	rpr_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_rpr_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	rxtorax_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_rxtorax_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	sespu_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_sespu_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	cultivo_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_cultivo_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	usg_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_usg_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	biopsia_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_biopsia_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	cita_medica = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_cita_medica',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	retiro_medicamento = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_retiro_medicamento',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Retiro de Medicamento')

	caviral_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_caviral_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	ppd_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_ppd_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	otro_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_otro_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	tupu_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tupu_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	tupu_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tupu_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	tupu_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tupu_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	tupu_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tupu_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	tupu_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tupu_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	tupu_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tupu_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	tudi_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tudi_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	tudi_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tudi_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	tudi_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tudi_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	tudi_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tudi_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	tudi_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tudi_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	tudi_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tudi_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	hepb_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepb_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	hepb_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepb_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	hepb_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepb_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	hepb_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepb_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	hepb_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepb_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	hepb_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepb_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')	

	hepc_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepc_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	hepc_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepc_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	hepc_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepc_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	hepc_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepc_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	hepc_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepc_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	hepc_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepc_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')


	ulg_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_ulg_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	ulg_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_ulg_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	ulg_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_ulg_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	ulg_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_ulg_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	ulg_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_ulg_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	ulg_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_ulg_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	secure_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_secure_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	secure_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_secure_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	secure_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_secure_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	secure_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_secure_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	secure_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_secure_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	secure_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_secure_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	fluva_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fluva_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	fluva_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fluva_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	fluva_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fluva_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	fluva_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fluva_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	fluva_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fluva_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	fluva_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fluva_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')


	buin_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_buin_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	buin_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_buin_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	buin_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_buin_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	buin_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_buin_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	buin_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_buin_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	buin_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_buin_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	edes_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_edes_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	edes_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_edes_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	edes_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_edes_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	edes_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_edes_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	edes_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_edes_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	edes_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_edes_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')


	verge_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_verge_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	verge_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_verge_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	verge_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_verge_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	verge_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_verge_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	verge_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_verge_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	verge_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_verge_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')



	trasex_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_trasex_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	trasex_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_trasex_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	trasex_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_trasex_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	trasex_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_trasex_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	trasex_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_trasex_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	trasex_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_trasex_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')


	proc_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_proc_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	proc_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_proc_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	proc_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_proc_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	proc_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_proc_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	proc_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_proc_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	proc_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_proc_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')


	infpel_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_infpel_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	infpel_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_infpel_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	infpel_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_infpel_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	infpel_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_infpel_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	infpel_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_infpel_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	infpel_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_infpel_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

class BoletaClinicaSeguimientoForm(ModelForm):
	class Meta:
		model = BoletasClinicas
		widgets = {
			'lic4_resultado': TextInput(attrs={'type': 'number'}),
			'caviral_resultado': TextInput(attrs={'type': 'number'}),
			'rxtorax_resultado': TextInput(attrs={'type': 'number'}),
		}
		fields = "__all__"
		exclude = ['hepb_resultado','rpr_resultado','creado_por', 'fecha_creacion', 'fecha_actualizacion', 'actualizado_por', 'hepc_resultado','estado_clinico','embarazada_vih','evaluacion_go','programacion_cesaria','afiliacion_seguridad_social','seguro_privado','relaciones_mismo_sexo','dinero_por_relaciones','identificacion_genero','lic4','lic4_ordenado_consulta','caviral','caviral_ordenado_consulta','hepb','hepb_ordenado_consulta','hepc','hepc_ordenado_consulta','rpr','rpr_ordenado_consulta','rxtorax','rxtorax_ordenado_consulta','sespu','sespu_ordenado_consulta','ppd','ppd_ordenado_consulta','cultivo','cultivo_ordenado_consulta','usg','usg_ordenado_consulta','biopsia','biopsia_ordenado_consulta','otro','otro_ordenado_consulta','tupu','tupu_initrat','tupu_entrat','tupu_entrat_fintrat','tupu_intrat','tupu_intrat_reitrat','tupu_trat','tudi','tudi_initrat','tudi_entrat','tudi_entrat_fintrat','tudi_intrat','tudi_intrat_reitrat','tudi_trat','hepb','hepb_initrat','hepb_entrat','hepb_entrat_fintrat','hepb_intrat','hepb_intrat_reitrat','hepb_trat','hepc','hepc_initrat','hepc_entrat','hepc_entrat_fintrat','hepc_intrat','hepc_intrat_reitrat','hepc_trat','ulg','ulg_initrat','ulg_entrat','ulg_entrat_fintrat','ulg_intrat','ulg_intrat_reitrat','ulg_trat','secure','secure_initrat','secure_entrat','secure_entrat_fintrat','secure_intrat','secure_intrat_reitrat','secure_trat','fluva','fluva_initrat','fluva_entrat','fluva_entrat_fintrat','fluva_intrat','fluva_intrat_reitrat','fluva_trat','buin','buin_initrat','buin_entrat','buin_entrat_fintrat','buin_intrat','buin_intrat_reitrat','buin_trat','edes','edes_initrat','edes_entrat','edes_entrat_fintrat','edes_intrat','edes_intrat_reitrat','edes_trat','verge','verge_initrat','verge_entrat','verge_entrat_fintrat','verge_intrat','verge_intrat_reitrat','verge_trat','trasex','trasex_initrat','trasex_entrat','trasex_entrat_fintrat','trasex_intrat','trasex_intrat_reitrat','trasex_trat','proc','proc_initrat','proc_entrat','proc_entrat_fintrat','proc_intrat','proc_intrat_reitrat','proc_trat','infpel','infpel_initrat','infpel_entrat','infpel_entrat_fintrat','infpel_intrat','infpel_intrat_reitrat','infpel_tra','actualizado_por', 'creado_por', 'fecha_creacion', 'fecha_actualizacion', 'boleta', 'establecimiento']
	
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
	
	hepb_resultado =  forms.ChoiceField(widget=RadioSelect, choices=RESULTADOS, label='Resultado', required=False, initial=None)
	hepc_resultado =  forms.ChoiceField(widget=RadioSelect, choices=RESULTADOS, label='Resultado', required=False, initial=None)
	rpr_resultado =  forms.ChoiceField(widget=RadioSelect, choices=RESULTADOS, label='Resultado', required=False, initial=None)
	
	actualmente_tarv =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Actualmente TARV', required=False, initial=None)
	estatus_actual_tarv =  forms.ChoiceField(widget=RadioSelect, choices=STATUS_TARV, label='', required=False, initial=None)

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
	usg =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='USG(Ultrasograma)', required=False, initial=None)
	usg_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False, initial=None)
	biopsia =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Biopsia', required=False, initial=None)
	biopsia_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False, initial=None)
	otro =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Otro', required=False, initial=None)
	otro_ordenado_consulta =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='Ordenados en esta consulta', required=False, initial=None)
	tupu =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='TUBERCULOSIS PULMONAR', required=False, initial=None)
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
	secure =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='SINDROME SECRECION URETAL', required=False, initial=None)
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

	lic4_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_lic4_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	hepb_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepb_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	hepc_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepc_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	rpr_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_rpr_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	rxtorax_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_rxtorax_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	sespu_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_sespu_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	cultivo_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_cultivo_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	usg_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_usg_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	biopsia_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_biopsia_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	cita_medica = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_cita_medica',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	retiro_medicamento = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_retiro_medicamento',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Retiro de Medicamento')

	caviral_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_caviral_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	ppd_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_ppd_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	otro_fecha_realizacion = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_otro_fecha_realizacion',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Realización')

	tupu_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tupu_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	tupu_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tupu_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	tupu_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tupu_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	tupu_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tupu_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	tupu_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tupu_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	tupu_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tupu_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	tudi_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tudi_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	tudi_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tudi_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	tudi_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tudi_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	tudi_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tudi_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	tudi_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tudi_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	tudi_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tudi_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	hepb_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepb_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	hepb_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepb_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	hepb_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepb_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	hepb_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepb_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	hepb_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepb_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	hepb_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepb_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')	

	hepc_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepc_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	hepc_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepc_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	hepc_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepc_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	hepc_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepc_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	hepc_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepc_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	hepc_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_hepc_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')


	ulg_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_ulg_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	ulg_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_ulg_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	ulg_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_ulg_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	ulg_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_ulg_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	ulg_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_ulg_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	ulg_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_ulg_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	secure_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_secure_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	secure_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_secure_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	secure_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_secure_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	secure_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_secure_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	secure_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_secure_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	secure_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_secure_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	fluva_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fluva_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	fluva_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fluva_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	fluva_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fluva_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	fluva_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fluva_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	fluva_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fluva_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	fluva_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fluva_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')


	buin_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_buin_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	buin_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_buin_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	buin_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_buin_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	buin_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_buin_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	buin_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_buin_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	buin_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_buin_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	edes_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_edes_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	edes_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_edes_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	edes_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_edes_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	edes_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_edes_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	edes_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_edes_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	edes_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_edes_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')


	verge_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_verge_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	verge_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_verge_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	verge_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_verge_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	verge_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_verge_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	verge_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_verge_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	verge_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_verge_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')



	trasex_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_trasex_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	trasex_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_trasex_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	trasex_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_trasex_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	trasex_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_trasex_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	trasex_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_trasex_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	trasex_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_trasex_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')


	proc_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_proc_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	proc_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_proc_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	proc_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_proc_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	proc_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_proc_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	proc_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_proc_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	proc_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_proc_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')


	infpel_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_infpel_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Diagnóstico')

	infpel_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_infpel_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	infpel_entrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_infpel_entrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	infpel_entrat_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_infpel_entrat_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	infpel_intrat_diag = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_infpel_intrat_diag',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	infpel_intrat_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_infpel_intrat_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')



class BoletaSeguimientoForm(ModelForm):
	class Meta:
		model = BoletasSeguimientos
		widgets = {
			'lic4_resultado': TextInput(attrs={'type': 'number'}),
			'caviral_resultado': TextInput(attrs={'type': 'number'}),
			'rxtorax_resultado': TextInput(attrs={'type': 'number'}),
		}
		fields = "__all__"
		exclude = ['azt','abc','efv','rpv','dtf','lpv', 'boleta_clinica', 'identidad', 'creado_por', 'fecha_creacion', 'fecha_actualizacion', 'actualizado_por',
			'abc_med', 'ft_med', 'd4t_med', 'azt_med', 'efv_med', 'nvp_med', 'ddi_med', 'tc_med', 'tdf_med', 'rpv_med', 'etr_med', 'atv_med', 'drv_med', 'fpv_med', 'idv_med', 'nfv_med', 'sqv_med', 'tpv_med', 'ral_med', 'evg_med', 'dtg_med', 
			'abc_ter', 'ft_ter', 'd4t_ter', 'azt_ter', 'efv_ter', 'nvp_ter', 'ddi_ter', 'tc_ter', 'tdf_ter', 'rpv_ter', 'etr_ter', 'atv_ter', 'drv_ter', 'fpv_ter', 'idv_ter', 'nfv_ter', 'sqv_ter', 'tpv_ter', 'ral_ter', 'evg_ter', 'dtg_ter'
		]
	conteo_cd4 =  forms.ChoiceField(widget=RadioSelect, choices=CONTEO, label='Conteo de CD4 con que Inició el Terapia', required=False, initial=None)
	causa_fallecido =  forms.ChoiceField(widget=RadioSelect, choices=MOTIVOS_FALLECIMIENTO, label='Causa del Fallecimiento', required=False, initial=None)
	motivo =  forms.ChoiceField(widget=RadioSelect, choices=MOTIVOS_CONSULTA, label='Motivo de Consulta', required=False, initial=None)
	profpri =  forms.ChoiceField(widget=RadioSelect, choices=ORDENADOS_EN_CONSULTA, label='PROFILAXIS PRIMARIA', required=False, initial=None)
	tmpsmx =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='PROFILAXIS CON TMPSMX', required=False, initial=None)
	tmpsmx_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False, initial=None)
	tmpsmx_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False, initial=None)
	tmpsmx_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpió Tratamiento', required=False, initial=None)
	tmpsmx_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinició Tratamiento', required=False, initial=None)

	isoniacida =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='PROFILAXIS CON ISONIAZIDA', required=False, initial=None)
	isoniacida_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False, initial=None)
	isoniacida_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False, initial=None)
	isoniacida_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpió Tratamiento', required=False, initial=None)
	isoniacida_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinició Tratamiento', required=False, initial=None)

	azitromicida =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='PROFILAXIS CON AZITROMICIDA', required=False, initial=None)
	azitromicida_initrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Inició Tratamiento', required=False, initial=None)
	azitromicida_fintrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Finalizó Tratamiento', required=False, initial=None)
	azitromicida_intrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Interrumpió Tratamiento', required=False, initial=None)
	azitromicida_reitrat =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Reinició Tratamiento', required=False, initial=None)
	
	esquema_arv =  forms.ChoiceField(widget=RadioSelect, choices=ESQUEMA_ARV, label='Esquema ARV', required=False, initial=None)
	cambio_terapia =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Cambio de Terapia', required=False, initial=None)
	motivo_cambio_terapia =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Fracaso Terapeutico (Resistencia a los ARV)', required=False, initial=None)
	documentado_con =  forms.ChoiceField(widget=RadioSelect, choices=DOCUMENTADO, label='Documentado por', required=False, initial=None)
	esquema_actual_arv =  forms.ChoiceField(widget=RadioSelect, choices=ESQUEMA_ARV, label='Esquema Actual ARV', required=False, initial=None)
	
	abandono =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Abandono', required=False, initial=None)
	suspension =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Suspensión', required=False, initial=None)
	activo =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Activo', required=False, initial=None)
	fallecido =  forms.ChoiceField(widget=RadioSelect, choices=SI_NO, label='Fallecido', required=False, initial=None)

	tmpsmx_fecha_intrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tmpsmx_fecha_intrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha Inicio TARV')

	fecha_consulta = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fecha_consulta',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Consulta')

	fecha_proxima_cita = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fecha_proxima_cita',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Próxima Cita')

	tmpsmx_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tmpsmx_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	tmpsmx_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tmpsmx_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	tmpsmx_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_tmpsmx_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	isoniacida_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_isoniacida_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	isoniacida_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_isoniacida_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	isoniacida_fecha_intrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_isoniacida_fecha_intrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	isoniacida_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_isoniacida_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	azitromicida_fecha_initrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_azitromicida_fecha_initrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	azitromicida_fecha_fintrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_azitromicida_fecha_fintrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	azitromicida_fecha_intrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_azitromicida_fecha_intrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	azitromicida_fecha_reitrat = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_azitromicida_fecha_reitrat',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha')

	arv_fecha_ini = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_arv_fecha_ini',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Inicio de ARV')

	fecha_abandono = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fecha_abandono',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Abandono')

	fecha_reinicio = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fecha_reinicio',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Reinicio')

	fecha_suspension = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fecha_suspension',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Suspensión')

	fecha_fallecido = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fecha_fallecido',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Fallecimiento')

	fecha_prescripcion_arv = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fecha_prescripcion_arv',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Prescripción de ARV')


	fecha_cambio_terapia = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fecha_cambio_terapia',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de  Cambio de Terapia')

	fecha_entrega_arv = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fecha_entrega_arv',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Entrega de ARV')

	fecha_proxentrega_arv = forms.CharField(widget=TextInputWithButton(btn_attrs={
	    'label': 'x',
	    'id': 'limpiar_fecha_proxentrega_arv',
	    'type': 'button',
	    'placement': 'append',
	}), required=False, label='Fecha de Próxima Entrega de ARV')




