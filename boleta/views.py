# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.urls import reverse

from django.db.models import Count

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
	embarazada = Condiciones.objects.get(nombre='Embarazada')
	#AJAX
	if request.is_ajax():
		identidad = request.GET['identidad']
		try:
			persona = RPN.objects.values('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'sexo', 'fecha_nacimiento').get(identidad=identidad)
		except Exception, e:
			persona = False

		return HttpResponse(json.dumps(persona, default=date_handler), content_type='application/json')
	
	#GET
	elif request.method == 'GET':
		formulario = RPNForm()
		formulario2 = BoletaForm()
		formulario3 = BoletaConsejeriaForm()
		ctx = {
			'formulario' : formulario,
			'formulario2': formulario2,
			'formulario3': formulario3,
			'embarazada': embarazada,
			'exito': exito,
		}
		return render(request, 'pre_prueba_vih.html', ctx)

	#POST
	elif request.method == 'POST':
		ide = request.POST['identidad']
		identidad = ide.replace("-", "")

		formulario = RPNForm(request.POST)
		formulario2 = BoletaForm(request.POST)
		formulario3 = BoletaConsejeriaForm(request.POST)
		print request.POST['expediente'], 'EXPEDIENTE', request.POST['fecha_nacimiento']
		if formulario2.is_valid() and formulario3.is_valid():
			try:
				registro = formulario2.save(commit=False)
				registro.expediente =  request.POST['expediente']
				registro.ciudad =  Ciudades.objects.get(pk=request.POST['ciudad'])
				registro.barrio =  Ciudades.objects.get(pk=request.POST['barrio'])
				registro.municipio =  Municipios.objects.get(pk=request.POST['municipio'])
				registro.identidad =  identidad
				registro.sexo =  request.POST['sexo']
				registro.primer_nombre =  request.POST['primer_nombre']
				registro.segundo_nombre =  request.POST['segundo_nombre']
				registro.primer_apellido =  request.POST['primer_apellido']
				registro.segundo_apellido =  request.POST['segundo_apellido']
				registro.fecha_nacimiento =  request.POST['fecha_nacimiento']
				registro.identidad_madre = request.POST['identidad_madre'].replace("-", "")
				registro.identidad_padre = request.POST['identidad_padre'].replace("-", "")
				registro.identidad_tutor = request.POST['identidad_tutor'].replace("-", "")
				registro.rpn =  True
				registro.creado_por = request.user
				registro.actualizado_por = request.user
				registro.save()

				registro2 = formulario3.save(commit=False)
				registro2.boleta = registro
				registro2.nombre_persona_solicitante = '%s %s %s %s'%(request.POST['primer_nombre'],request.POST['segundo_nombre'], request.POST['primer_apellido'], request.POST['segundo_apellido'])
				registro2.creado_por = request.user
				registro2.actualizado_por = request.user
				
				try:
					responsable = Responsables.objects.get(usuario_sistema=request.user)
					registro2.nombre_consejero = responsable.nombres + ' ' + responsable.primer_apellido + ' ' + responsable.segundo_apellido
				except Exception, e:
					registro2.nombre_consejero = request.user.first_name + ' ' + request.user.last_name
				
				registro2.save()
				formulario = RPNForm()
				formulario2 = BoletaForm()
				formulario3 = BoletaConsejeriaForm()
				exito = True
			except Exception, e:
				print e
		else:
			print 'PASO POR AQUI'
			pass
		ctx = {
			'formulario' : formulario,
			'formulario2': formulario2,
			'formulario3': formulario3,
			'embarazada': embarazada,
			'exito': exito,
		}
		return render(request, 'pre_prueba_vih.html', ctx)

def prueba_vih(request):
	exito = False
	#AJAX
	if request.is_ajax():
		identidad = request.GET['identidad']
		try:

			boleta = Boletas.objects.values(
				'expediente', 
				'pk',
				'primer_nombre', 
				'segundo_nombre', 
				'primer_apellido', 
				'segundo_apellido', 
				'sexo', 
				'fecha_nacimiento'
			).get(identidad=identidad)
			expediente = boleta['expediente']
			#boleta = boleta['pk']

			cantidad = BoletasPruebas.objects.filter(boleta__identidad=identidad)
			if not cantidad:
				cantidad_boleta = 1
			else:
				cantidad_boleta = int(cantidad.count()) + 1

			persona = True
		except Exception, e:
			print 'ERROR' , e
			persona = False
			expediente = False
			cantidad_boleta = False
			boleta = False


		data = {
			'persona' : persona,
			'expediente': expediente,
			'numero_prueba' : cantidad_boleta,
			'boleta' : boleta,
		}
		return HttpResponse(json.dumps(data, default=date_handler), content_type='application/json')

	#GET
	elif request.method == 'GET':
		formulario = BoletaPruebaForm()
		ctx = {
			'formulario' : formulario,
			'exito': exito,
		}
		return render(request, 'prueba_vih.html', ctx)

	#POST
	elif request.method == 'POST':
		print 'aksjhdkajshdkasd',request.POST['boleta']
		formulario = BoletaPruebaForm(request.POST)
		if formulario.is_valid():
			registro = formulario.save(commit=False)
			registro.boleta =  Boletas.objects.get(pk=request.POST['boleta'])
			registro.creado_por = request.user
			registro.actualizado_por = request.user
			registro.save()

			formulario = BoletaPruebaForm()
			exito = True
		else:
			pass

		ctx = {
			'formulario' : formulario,
			'exito': exito,
		}
		return render(request, 'prueba_vih.html', ctx)	

def post_prueba_vih(request):
	exito = False
	#AJAX
	if request.is_ajax():
		identidad = request.GET['identidad']
		try:

			boleta = dict(Boletas.objects.values(
				'primer_nombre', 
				'segundo_nombre', 
				'primer_apellido', 
				'segundo_apellido', 
				'sexo', 
				'expediente', 'pk', 'nombre_madre', 'nombre_padre', 'nombre_tutor', 'edad_anios'
			).get(identidad=identidad))
			expediente = boleta['expediente']
			persona = True

		except Exception, e:
			print 'ERROR',e
			persona = False
			expediente = False
			boleta = False


		data = {
			'persona' : persona,
			'expediente': expediente,
			'boleta' : boleta,
		}
		return HttpResponse(json.dumps(data, default=date_handler), content_type='application/json')
	
	#GET
	elif request.method == 'GET':
		formulario = BoletasConsejeriaPostPruebaForm()
		ctx = {
			'formulario' : formulario,
			'exito': exito,
		}
		return render(request, 'post_prueba_vih.html', ctx)

	#POST
	elif request.method == 'POST':
		formulario = BoletasConsejeriaPostPruebaForm(request.POST)
		if formulario.is_valid():
			try:
				responsable = Responsables.objects.get(usuario_sistema=request.user)
				responsable_nombre = responsable.nombres + ' ' + responsable.primer_apellido + ' ' + responsable.segundo_apellido
			except Exception, e:
				responsable_nombre = request.user.first_name + ' ' + request.user.last_name
			
			registro = formulario.save(commit=False)
			registro.nombre_consejero =  responsable_nombre
			registro.boleta =  Boletas.objects.get(pk=request.POST['boleta'])
			registro.creado_por = request.user
			registro.actualizado_por = request.user
			registro.save()

			formulario = BoletasConsejeriaPostPruebaForm()
			exito = True
		else:
			pass

		ctx = {
			'formulario' : formulario,
			'exito': exito,
		}
		return render(request, 'post_prueba_vih.html', ctx)	


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