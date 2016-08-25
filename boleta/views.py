from __future__ import unicode_literals

from django.shortcuts import render
from django.http import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.urls import reverse

from general.forms import *
from boleta.forms import *

import json
@login_required()
def principal(request):
	return render(request, 'principal.html')

def date_handler(obj):
    if hasattr(obj, 'isoformat'):
        return obj.isoformat()
    else:
        raise TypeError

@login_required()
def pre_prueba_vih(request):
	exito = False
	if request.is_ajax():
		identidad = request.GET['identidad']
		try:
			persona = RPN.objects.values('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'sexo', 'fecha_nacimiento').get(identidad=identidad)
		except Exception, e:
			persona = False

		return HttpResponse(json.dumps(persona, default=date_handler), content_type='application/json')
	elif request.method == 'GET':
		formulario = RPNForm()
		formulario2 = BoletaForm()
		formulario3 = BoletaConsejeriaForm()
		ctx = {
			'formulario' : formulario,
			'formulario2': formulario2,
			'formulario3': formulario3,
			'exito': exito,
		}
		return render(request, 'pre_prueba_vih.html', ctx)

def prueba_vih(request):
	exito = False
	if request.method == 'GET':
		formulario = BoletaPruebaForm()
		ctx = {
			'formulario' : formulario,
			'exito': exito,
		}
		return render(request, 'prueba_vih.html', ctx)

@login_required()
def ajax(request):
	if request.is_ajax():
		tabla = request.GET['tabla']
		valor = request.GET['valor']

		if tabla == 'municipio':
			data = list(Municipios.objects.values('id', 'codigo', 'nombre').filter(departamento=valor))
		elif tabla == 'ciudad':
			data = list(Ciudades.objects.values('id', 'codigo', 'nombre').filter(municipio=valor))
		elif tabla == 'barrio':
			data = list(Barrios.objects.values('id', 'codigo', 'nombre').filter(ciudad=valor))
		return HttpResponse(json.dumps(data, default=date_handler), content_type='application/json')