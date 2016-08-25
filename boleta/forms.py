# -*- coding: utf-8 -*-
from django.forms import ModelForm
from django.forms.widgets import *
from django import forms
from boleta.models import *
from general.models import *
from django.contrib.auth.models import User

ESTADO_CIVIL = (
	(1, "Soltero(a)"),
	(2, "Casado(a)"),
	(3, "Union Libre"),
)

RESULTADOS = (
	(1, "Positivo"),
	(2, "Negativo"),
)
class BoletaForm(ModelForm):
	class Meta:
		model = Boletas
		fields = "__all__"
		exclude = ['actualizado_por', 'creado_por', 'identidad', 'expediente', 'sexo', 'municipio', 'ciudad', 'barrio']
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
