# -*- encoding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import *
from django.urls import reverse
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.db.models import Count
from django.db import transaction, IntegrityError

from general.forms import *
from boleta.forms import *


import json

def usuario(id):
	return Responsables.objects.get(usuario=id)

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
	responsable = usuario(request.user.pk)
	embarazada = Condiciones.objects.get(nombre='Embarazada')
	#AJAX
	if request.is_ajax():
		identidad = request.GET['identidad']
		try:
			persona = dict(RPN.objects.values('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'sexo', 'fecha_nacimiento').get(identidad=identidad))
			query = BoletasConsejeria.objects.filter(boleta__identidad=identidad)
			periodicidad = query.count()
		except Exception, e:
			persona = False
			periodicidad = 0

		data = {
			'persona': persona,
			'periodicidad': periodicidad
		}
		return HttpResponse(json.dumps(persona, default=date_handler), content_type='application/json')
	
	#GET
	elif request.method == 'GET':
		formulario = RPNForm()
		formulario.fields['sexo'].widget.attrs['disabled'] = True
		formulario2 = BoletaForm()
		formulario3 = BoletaConsejeriaForm()
		ctx = {
			'formulario' : formulario,
			'formulario2': formulario2,
			'formulario3': formulario3,
			'embarazada': embarazada,
			'exito': exito,
			'responsable': responsable,
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
				formulario.fields['sexo'].widget.attrs['disabled'] = True

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
			'responsable': responsable,
		}
		return render(request, 'pre_prueba_vih.html', ctx)

@login_required()
def prueba_vih(request):
	exito = False
	responsable = usuario(request.user.pk)
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
			'responsable': responsable,
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
			'responsable': responsable,
		}
		return render(request, 'prueba_vih.html', ctx)	

@login_required()
def post_prueba_vih(request):
	exito = False
	responsable = usuario(request.user.pk)
	#AJAX
	if request.is_ajax():
		identidad = request.GET['identidad']
		try:

			boleta = dict(BoletasPruebas.objects.values(
				'boleta__primer_nombre', 
				'boleta__segundo_nombre', 
				'boleta__primer_apellido', 
				'boleta__segundo_apellido', 
				'boleta__sexo', 
				'boleta__expediente', 
				'boleta__pk', 
				'boleta__nombre_madre', 
				'boleta__nombre_padre', 
				'boleta__nombre_tutor', 
				'boleta__edad_anios',
				'resultado_prueba_tamizaje',
				'resultado_prueba_confirmatoria',
			).get(boleta__identidad=identidad))
			expediente = boleta['boleta__expediente']
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
			'responsable': responsable,
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
			'responsable': responsable,
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

@transaction.atomic
@login_required()
def listado_asistencia(request):
	responsable = usuario(request.user.pk)
	exito = False
	#GET
	if request.method == 'GET':
		formulario = AsistenciaForm()
		ctx = {
			'formulario' : formulario,
			'exito': exito,
			'responsable': responsable,
		}
		return render(request, 'listado_asistencia.html', ctx)
	if request.method == 'POST':
		try:
			with transaction.atomic():
				identidades = request.POST.getlist('identidad[]')
				formulario = AsistenciaForm(request.POST)
				if formulario.is_valid():
					registro = formulario.save(commit=False)
					registro.creado_por = request.user
					registro.actualizado_por = request.user
					registro.save()

					for identidad in identidades:
						asistencia = ListadoAsistencia()
						asistencia.asistencia = registro
						asistencia.identidad = identidad
						asistencia.nombres = request.POST['nombre[' + identidad + ']']
						asistencia.correo_electronico = request.POST['correo[' + identidad+']']
						asistencia.edad = request.POST['edad['+identidad+']']
						asistencia.telefono = request.POST['telefono['+identidad+']']
						asistencia.cantidad_condones = request.POST['cantidad['+identidad+']']

						asistencia.save()

					formulario = AsistenciaForm()
					exito = True
				else:
					pass

				
		except Exception, e:
			print 'ERROR', e
		ctx = {
			'formulario' : formulario,
			'exito': exito,
			'responsable': responsable,
		}	
		return render(request, 'listado_asistencia.html', ctx)


@transaction.atomic
@login_required()
def boleta_clinica(request):
	responsable = usuario(request.user.pk)
	embarazada = Condiciones.objects.get(nombre='Embarazada')
	exito = False
	#AJAX
	if request.is_ajax():
		identidad = request.GET['identidad']
		try:
			persona = dict(
				Boletas.objects.values(
					'primer_nombre', 
					'segundo_nombre', 
					'primer_apellido', 
					'segundo_apellido', 
					'sexo', 
					'fecha_nacimiento',
					'edad_anios',
					'edad_meses',
					'pseudonimo',
					'estado_civil',
					'telefono_fijo',
					'telefono_celular',
					'ocupacion__pk',
					'departamento__pk',
					'municipio__pk',
					'calle',
					'bloque',
					'numero_casa',
					'referencias',
					'grupo_etnico__pk',
					'otro_grupo_etnico',
					'identidad_madre',
					'nombre_madre',
					'telefono_madre',
					'identidad_padre',
					'nombre_padre',
					'telefono_padre',
					'identidad_tutor',
					'nombre_tutor',
					'telefono_tutor',
					'direccion_tutor',
					'poblacion__pk',
					'actividad_economica__pk',
					'fecha_ultima_menstruacion',
					'ciudad__pk',
					'barrio__pk',
					'condiciones',
					'otro_condicion',
				).get(identidad=identidad)
			)
		except Exception, e:
			print e
			try:
				persona = dict(RPN.objects.values('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'sexo', 'fecha_nacimiento').get(identidad=identidad))
			except Exception, e:
				persona = False

		return HttpResponse(json.dumps(persona, default=date_handler), content_type='application/json')
	#GET
	elif request.method == 'GET':
		formulario = RPNForm()
		formulario2 = BoletaForm()
		formulario3 = BoletaClinicaForm()
		ctx = {
			'formulario' : formulario,
			'formulario2' : formulario2,
			'formulario3' : formulario3,
			'exito': exito,
			'responsable': responsable,
			'embarazada': embarazada,
		}
		return render(request, 'boleta_clinica.html', ctx)
	if request.method == 'POST':
		try:
			with transaction.atomic():
				identidades = request.POST.getlist('identidad[]')
				formulario = AsistenciaForm(request.POST)
				if formulario.is_valid():
					registro = formulario.save(commit=False)
					registro.creado_por = request.user
					registro.actualizado_por = request.user
					registro.save()

					for identidad in identidades:
						asistencia = ListadoAsistencia()
						asistencia.asistencia = registro
						asistencia.identidad = identidad
						asistencia.nombres = request.POST['nombre[' + identidad + ']']
						asistencia.correo_electronico = request.POST['correo[' + identidad+']']
						asistencia.edad = request.POST['edad['+identidad+']']
						asistencia.telefono = request.POST['telefono['+identidad+']']
						asistencia.cantidad_condones = request.POST['cantidad['+identidad+']']

						asistencia.save()

					formulario = AsistenciaForm()
					exito = True
				else:
					pass
		except Exception, e:
			print 'ERROR', e
		ctx = {
			'formulario' : formulario,
			'exito': exito,
			'responsable': responsable,
		}	
		return render(request, 'boleta_clinica.html', ctx)