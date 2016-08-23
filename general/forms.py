# -*- coding: utf-8 -*-
from django.forms import ModelForm
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
		widgets = {
			'sexo': RadioSelect(attrs={'class': 'iCheck'}),
		}

class RPNForm(ModelForm):
	class Meta:
		model = RPN
		exclude = ['estado_civil', 'fotografia', 'identidad']