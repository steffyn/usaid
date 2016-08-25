# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm, TextInput 
from django.forms.widgets import *
from general.models import *
from django.contrib.auth.models import User

class UsuarioForm(ModelForm):
	class Meta:
		model = User
		fields = ['username', 'password']

class UsuarioResponsableForm(ModelForm):
	class Meta:
		model = Responsables
		fields = "__all__"
		exclude = ['usuario_sistema', 'activo']
	

class RPNForm(ModelForm):
	class Meta:
		model = RPN
		exclude = ['estado_civil', 'fotografia', 'identidad']

		widgets = {
			'primer_nombre': TextInput(attrs={'readonly': 'readonly'}),
			'segundo_nombre': TextInput(attrs={'readonly': 'readonly'}),
			'primer_apellido': TextInput(attrs={'readonly': 'readonly'}),
			'segundo_apellido': TextInput(attrs={'readonly': 'readonly'}),
			'fecha_nacimiento': TextInput(attrs={'disabled': 'readonly'}),
		}
	sexo =  forms.ChoiceField(choices=GENERO, widget=RadioSelect)