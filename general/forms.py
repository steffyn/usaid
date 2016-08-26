# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, TextInput 
from django.forms.widgets import *
from general.models import *
from django.contrib.auth.models import User

class UsuarioForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password', 'groups']
		widgets = {
			'password': TextInput(attrs={'type': 'password'}),
		}

class UsuarioResponsableForm(ModelForm):
	class Meta:
		model = Responsables
		fields = "__all__"
		exclude = ['usuario_sistema', 'activo']
	sexo =  forms.ChoiceField(choices=GENERO, widget=RadioSelect)
	

class RPNForm(ModelForm):
	class Meta:
		model = RPN
		exclude = ['estado_civil', 'fotografia', 'identidad']

		widgets = {
			'primer_nombre': TextInput(attrs={'readonly': 'readonly', 'required': 'required'}),
			'segundo_nombre': TextInput(attrs={'readonly': 'readonly'}),
			'primer_apellido': TextInput(attrs={'readonly': 'readonly', 'required': 'required'}),
			'segundo_apellido': TextInput(attrs={'readonly': 'readonly'}),
			'fecha_nacimiento': TextInput(attrs={'disabled': 'readonly', 'required': 'required'}),
		}
	sexo =  forms.ChoiceField(choices=GENERO, widget=RadioSelect)