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
import datetime
import calendar

def usuario(id):
	return Responsables.objects.get(usuario_sistema__id=id)

def date_handler(obj):
	if hasattr(obj, 'isoformat'):
		return obj.isoformat()
	else:
		raise TypeError



def add_months(sourcedate,months):
	import datetime
	month = sourcedate.month - 1 + months
	year = int(sourcedate.year + month / 12 )
	month = month % 12 + 1
	day = min(sourcedate.day,calendar.monthrange(year,month)[1])
	return datetime.date(year,month,day)

def identidad(request):
	identidad = request.GET['identidad']
	try:
		persona = dict(RPN.objects.values('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'sexo', 'fecha_nacimiento').get(identidad=identidad))
		query = BoletasConsejeria.objects.filter(boleta__identidad=identidad)
		periodicidad = query.count()
	except Exception, e:
		persona = False
		periodicidad = 0
		
	return HttpResponse(json.dumps(persona, default=date_handler), content_type='application/json')

@login_required()
def pre_prueba_vih(request):
	exito = False
	error = False
	try:
		responsable = usuario(request.user.pk)
	except Exception, e:
		responsable = ''

	try:
		embarazada = Condiciones.objects.get(nombre='Embarazada')
	except Exception, e:
		embarazada = ''
	#AJAX
	if request.is_ajax():
		identidad = request.GET['identidad']
		
		#VALIDACIONES DONDE SI TIENE BOLETA INGRESADA MAYOR DE 3
		hoy = datetime.today().date()
		try:
			ultima_boleta = Boletas.objects.filter(identidad=identidad).order_by('-fecha_actualizacion')[:1].get()
			fecha = add_months(ultima_boleta.fecha_actualizacion, 3)
			if fecha > hoy:
				persona = 'existe'
			else:
				try:
					persona = dict(RPN.objects.values('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'sexo', 'fecha_nacimiento').get(identidad=identidad))
					query = BoletasConsejeria.objects.filter(boleta__identidad=identidad)
					periodicidad = query.count()
				except Exception, e:
					persona = False
					periodicidad = 0
		except Exception, e:
			try:
				persona = dict(RPN.objects.values('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'sexo', 'fecha_nacimiento').get(identidad=identidad))
				query = BoletasConsejeria.objects.filter(boleta__identidad=identidad)
				periodicidad = query.count()
			except Exception, e:
				persona = False
				periodicidad = 0
			
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
		if request.POST.get('identidad') == '' or request.POST.get('primer_nombre') == '' or request.POST.get('primer_apellido') == '':
			formulario = RPNForm(request.POST)
			formulario2 = BoletaForm(request.POST)
			formulario3 = BoletaConsejeriaForm(request.POST)
			ctx = {
				'formulario' : formulario,
				'formulario2': formulario2,
				'formulario3': formulario3,
				'embarazada': embarazada,
				'error': 'LOS DATOS GENERALES NO PUEDEN IR VACIOS, PORFAVOR REVISARLOS.',
				'responsable': responsable,
			}
			return render(request, 'pre_prueba_vih.html', ctx)

		ide = request.POST['identidad']
		identidad = ide.replace("-", "")
		
		formulario = RPNForm()
		formulario2 = BoletaForm(request.POST)
		formulario3 = BoletaConsejeriaForm(request.POST)
		if formulario2.is_valid() and formulario3.is_valid():
			try:
				registro = formulario2.save(commit=False)
				registro.expediente =  identidad +'-'+ request.POST['fecha_nacimiento'] +'-'+ request.POST['sexo_persona']
				registro.grupo_etnico =  None if request.POST.get('grupo_etnico') == '' or request.POST.get('grupo_etnico') == None else GruposEtnicos.objects.get(pk=request.POST.get('grupo_etnico'))
				try:
					registro.ciudad =  Ciudades.objects.get(pk=request.POST['ciudad'])
				except Exception, e:
					registro.ciudad =  None
				try:
					registro.municipio =  Municipios.objects.get(pk=request.POST['municipio'])
				except Exception, e:
					registro.municipio =  None
				
				registro.identidad =  identidad
				registro.sexo =  request.POST['sexo_persona']
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

				if request.user.has_perm('boleta.ingresar_establecimiento'):
					registro.establecimiento = Establecimientos.objects.get(pk=request.POST['establecimiento'])
				else:
					try:
						responsable = Responsables.objects.get(usuario_sistema=request.user)
						registro.establecimiento = responsable.establecimiento
					except Exception, e:
						registro.establecimiento = None

				registro.save()
				formulario2.save_m2m()

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
				error= 'Se genero un error al guardar los datos, revise bien el formulario. Si no contactese con el Administrador.',e
		else:
			error = 'Hay un error en el formulario, por favor revise los datos ingresados'
		ctx = {
			'formulario' : formulario,
			'formulario2': formulario2,
			'formulario3': formulario3,
			'embarazada': embarazada,
			'exito': exito,
			'error':error,
			'responsable': responsable,
		}
		return render(request, 'pre_prueba_vih.html', ctx)

@login_required()
def prueba_vih(request):
	exito = False
	try:
		responsable = usuario(request.user.pk)
	except Exception, e:
		responsable = ''
	#AJAX
	if request.is_ajax():
		identidad = request.GET['identidad']
		#VALIDACIONES DONDE SI TIENE BOLETA INGRESADA MAYOR DE 3
		hoy = datetime.today().date()
		print hoy
		try:
			ultima_boleta = BoletasPruebas.objects.filter(boleta__identidad=identidad).order_by('-fecha_actualizacion')[:1].get()
			fecha = add_months(ultima_boleta.fecha_actualizacion, 3)
			if fecha > hoy:
				persona = 'existe'
				expediente = False
				cantidad_boleta = False
				boleta = False
			else:
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
					).filter(identidad=identidad).order_by('-fecha_actualizacion')[:1].get()
					expediente = boleta['expediente']

					cantidad = BoletasPruebas.objects.filter(boleta__identidad=identidad)
					if not cantidad:
						cantidad_boleta = 1
					else:
						cantidad_boleta = int(cantidad.count()) + 1

					persona = True
				except Exception, e:
					print e
					persona = False
					expediente = False
					cantidad_boleta = False
					boleta = False
		except Exception, e:
			print 'ERROR',e	
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
				).filter(identidad=identidad).order_by('-fecha_actualizacion')[:1].get()
				expediente = boleta['expediente']
				#boleta = boleta['pk']

				cantidad = BoletasPruebas.objects.filter(boleta__identidad=identidad)
				if not cantidad:
					cantidad_boleta = 1
				else:
					cantidad_boleta = int(cantidad.count()) + 1

				persona = True
			except Exception, e:
				print e
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
		try:
			Boletas.objects.get(pk=request.POST['boleta'])
		except Exception as e:
			formulario = BoletaPruebaForm(request.POST)
			ctx = {
				'formulario' : formulario,
				'error': 'La identidad ingresada no tiene una boleta activa, por favor revisar los datos ingresados o de click a la lupa para buscar la boleta',
				'responsable': responsable,
				'identidad':request.POST['identidad']
			}
			return render(request, 'prueba_vih.html', ctx)	

		formulario = BoletaPruebaForm(request.POST)
		if formulario.is_valid():
			registro = formulario.save(commit=False)
			registro.boleta =  Boletas.objects.get(pk=request.POST['boleta'])
			registro.resultado_prueba_confirmatoria = None if request.POST.get('resultado_prueba_confirmatoria') == None or request.POST.get('resultado_prueba_confirmatoria') == '' else request.POST.get('resultado_prueba_confirmatoria')
			registro.creado_por = request.user
			registro.institucion_prueba_confirmatoria = None if responsable == '' else responsable.establecimiento.pk
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
	try:
		responsable = usuario(request.user.pk)
	except Exception, e:
		responsable = ''
	#AJAX
	if request.is_ajax():
		identidad = request.GET['identidad']
		#VALIDACIONES DONDE SI TIENE BOLETA INGRESADA MAYOR DE 3
		hoy = datetime.today().date()
		try:
			ultima_boleta = BoletasConsejeriaPostPrueba.objects.filter(boleta__identidad=identidad).order_by('-fecha_actualizacion')[:1].get()
			
			fecha = add_months(ultima_boleta.fecha_actualizacion, 3)
			if fecha > hoy:
				persona = 'existe'
				expediente = False
				cantidad_boleta = False
				boleta = False
			else:
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
					).filter(boleta__identidad=identidad).order_by('-fecha_actualizacion')[:1].get())
					expediente = boleta['boleta__expediente']
					persona = True

				except Exception, e:
					print e
					persona = False
					expediente = False
					boleta = False
		except Exception, e:
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
				).filter(boleta__identidad=identidad).order_by('-fecha_actualizacion')[:1].get())
				expediente = boleta['boleta__expediente']
				persona = True

			except Exception, e:
				print e
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
		try:
			Boletas.objects.get(pk=request.POST['boleta'])
		except Exception as e:
			formulario = BoletasConsejeriaPostPruebaForm(request.POST)
			ctx = {
				'formulario' : formulario,
				'error': 'La identidad ingresada no tiene una boleta activa, por favor revisar los datos ingresados o de click a la lupa para buscar la boleta',
				'responsable': responsable,
				'identidad':request.POST['identidad']
			}
			return render(request, 'post_prueba_vih.html', ctx)	

		formulario = BoletasConsejeriaPostPruebaForm(request.POST)
		if formulario.is_valid():
			try:
				responsable = Responsables.objects.get(usuario_sistema=request.user)
				responsable_nombre = responsable.nombres + ' ' + responsable.primer_apellido + ' ' + responsable.segundo_apellido
			except Exception, e:
				responsable_nombre = request.user.first_name + ' ' + request.user.last_name
			
			registro = formulario.save(commit=False)
			registro.nombre_consejero =  responsable_nombre
			registro.resultado_prueba_confirmatoria =  None if request.POST.get('resultado_prueba_confirmatoria') == None and request.POST.get('resultado_prueba_confirmatoria') == '' else request.POST.get('resultado_prueba_confirmatoria')
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
		return HttpResponse(json.dumps(data, default=date_handler), content_type='application/json')

@transaction.atomic
@login_required()
def listado_asistencia(request):
	try:
		responsable = usuario(request.user.pk)
	except Exception, e:
		responsable = ''
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
		identidades = request.POST.getlist('identidad[]')
		if len(identidades) == 0:
			formulario = AsistenciaForm(request.POST)
			ctx = {
				'formulario' : formulario,
				'error': 'Porfavor ingrese al menos un participante',
				'responsable': responsable,
			}	
			return render(request, 'listado_asistencia.html', ctx)
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
			pass
		ctx = {
			'formulario' : formulario,
			'exito': exito,
			'responsable': responsable,
		}	
		return render(request, 'listado_asistencia.html', ctx)


@transaction.atomic
@login_required()
def boleta_clinica(request):
	try:
		responsable = usuario(request.user.pk)
	except Exception, e:
		responsable = ''

	try:
		embarazada = Condiciones.objects.get(nombre='Embarazada')
	except Exception, e:
		embarazada = ''
	exito = False
	#AJAX
	if request.is_ajax():
		identidad = request.GET['identidad']
		try:
			persona = dict(
				Boletas.objects.values(
					'id',
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
					'barrio',
					'otro_condicion',
				).filter(identidad=identidad).order_by('-fecha_actualizacion')[:1].get()
			)
			try:
				clinica = dict(
					BoletasClinicas.objects.values(
						'id',
						'boleta__identidad', 
						'boleta__primer_nombre', 
						'boleta__segundo_nombre', 
						'boleta__primer_apellido', 
						'boleta__segundo_apellido', 
						'boleta__sexo', 
						'boleta__fecha_nacimiento',
						'boleta__edad_anios',
						'boleta__edad_meses',
						'boleta__edad_dias',
						'estado_inmunologico',
						'estado_clinico',
						'estadio_infeccion',
						'lic4',
						'lic4_resultado',
						'lic4_fecha_realizacion',
						'lic4_ordenado_consulta',
						'caviral',
						'caviral_resultado',
						'caviral_fecha_realizacion',
						'caviral_ordenado_consulta',
						'hepb',
						'hepb_resultado',
						'hepb_fecha_realizacion',
						'hepb_ordenado_consulta',
						'hepc',
						'hepc_resultado',
						'hepc_fecha_realizacion',
						'hepc_ordenado_consulta',
						'rpr',
						'rpr_resultado',
						'rpr_fecha_realizacion',
						'rpr_ordenado_consulta',
						'rxtorax',
						'rxtorax_resultado',
						'rxtorax_fecha_realizacion',
						'rxtorax_ordenado_consulta',
						'sespu',
						'sespu_resultado',
						'sespu_fecha_realizacion',
						'sespu_ordenado_consulta',
						'ppd',
						'ppd_resultado',
						'ppd_fecha_realizacion',
						'ppd_ordenado_consulta',
						'cultivo',
						'cultivo_resultado',
						'cultivo_fecha_realizacion',
						'cultivo_ordenado_consulta',
						'usg',
						'usg_resultado',
						'usg_fecha_realizacion',
						'usg_ordenado_consulta',
						'biopsia',
						'biopsia_resultado',
						'biopsia_fecha_realizacion',
						'biopsia_ordenado_consulta',
						'otro',
						'otro_resultado',
						'otro_fecha_realizacion',
						'otro_ordenado_consulta',
						'tupu',
						'tupu_diag',
						'tupu_initrat',
						'tupu_fecha_initrat',
						'tupu_entrat',
						'tupu_entrat_diag',
						'tupu_entrat_fintrat',
						'tupu_entrat_fecha_fintrat',
						'tupu_intrat',
						'tupu_intrat_diag',
						'tupu_intrat_reitrat',
						'tupu_intrat_fecha_reitrat',
						'tupu_trat',
						'tudi',
						'tudi_diag',
						'tudi_initrat',
						'tudi_fecha_initrat',
						'tudi_entrat',
						'tudi_entrat_diag',
						'tudi_entrat_fintrat',
						'tudi_entrat_fecha_fintrat',
						'tudi_intrat',
						'tudi_intrat_diag',
						'tudi_intrat_reitrat',
						'tudi_intrat_fecha_reitrat',
						'hepb',
						'hepb_diag',
						'hepb_initrat',
						'hepb_fecha_initrat',
						'hepb_entrat',
						'hepb_entrat_diag',
						'hepb_entrat_fintrat',
						'hepb_entrat_fecha_fintrat',
						'hepb_intrat',
						'hepb_intrat_diag',
						'hepb_intrat_reitrat',
						'hepb_intrat_fecha_reitrat',
						'hepc',
						'hepc_diag',
						'hepc_initrat',
						'hepc_fecha_initrat',
						'hepc_entrat',
						'hepc_entrat_diag',
						'hepc_entrat_fintrat',
						'hepc_entrat_fecha_fintrat',
						'hepc_intrat',
						'hepc_intrat_diag',
						'hepc_intrat_reitrat',
						'hepc_intrat_fecha_reitrat',
						'ulg',
						'ulg_diag',
						'ulg_initrat',
						'ulg_fecha_initrat',
						'ulg_entrat',
						'ulg_entrat_diag',
						'ulg_entrat_fintrat',
						'ulg_entrat_fecha_fintrat',
						'ulg_intrat',
						'ulg_intrat_diag',
						'ulg_intrat_reitrat',
						'ulg_intrat_fecha_reitrat',
						'secure',
						'secure_diag',
						'secure_initrat',
						'secure_fecha_initrat',
						'secure_entrat',
						'secure_entrat_diag',
						'secure_entrat_fintrat',
						'secure_entrat_fecha_fintrat',
						'secure_intrat',
						'secure_intrat_diag',
						'secure_intrat_reitrat',
						'secure_intrat_fecha_reitrat',
						'fluva',
						'fluva_diag',
						'fluva_initrat',
						'fluva_fecha_initrat',
						'fluva_entrat',
						'fluva_entrat_diag',
						'fluva_entrat_fintrat',
						'fluva_entrat_fecha_fintrat',
						'fluva_intrat',
						'fluva_intrat_diag',
						'fluva_intrat_reitrat',
						'fluva_intrat_fecha_reitrat',
						'buin',
						'buin_diag',
						'buin_initrat',
						'buin_fecha_initrat',
						'buin_entrat',
						'buin_entrat_diag',
						'buin_entrat_fintrat',
						'buin_entrat_fecha_fintrat',
						'buin_intrat',
						'buin_intrat_diag',
						'buin_intrat_reitrat',
						'buin_intrat_fecha_reitrat',
						'edes',
						'edes_diag',
						'edes_initrat',
						'edes_fecha_initrat',
						'edes_entrat',
						'edes_entrat_diag',
						'edes_entrat_fintrat',
						'edes_entrat_fecha_fintrat',
						'edes_intrat',
						'edes_intrat_diag',
						'edes_intrat_reitrat',
						'edes_intrat_fecha_reitrat',
						'verge',
						'verge_diag',
						'verge_initrat',
						'verge_fecha_initrat',
						'verge_entrat',
						'verge_entrat_diag',
						'verge_entrat_fintrat',
						'verge_entrat_fecha_fintrat',
						'verge_intrat',
						'verge_intrat_diag',
						'verge_intrat_reitrat',
						'verge_intrat_fecha_reitrat',
						'trasex',
						'trasex_diag',
						'trasex_initrat',
						'trasex_fecha_initrat',
						'trasex_entrat',
						'trasex_entrat_diag',
						'trasex_entrat_fintrat',
						'trasex_entrat_fecha_fintrat',
						'trasex_intrat',
						'trasex_intrat_diag',
						'trasex_intrat_reitrat',
						'trasex_intrat_fecha_reitrat',
						'proc',
						'proc_diag',
						'proc_initrat',
						'proc_fecha_initrat',
						'proc_entrat',
						'proc_entrat_diag',
						'proc_entrat_fintrat',
						'proc_entrat_fecha_fintrat',
						'proc_intrat',
						'proc_intrat_diag',
						'proc_intrat_reitrat',
						'proc_intrat_fecha_reitrat',
						'infpel',
						'infpel_diag',
						'infpel_initrat',
						'infpel_fecha_initrat',
						'infpel_entrat',
						'infpel_entrat_diag',
						'infpel_entrat_fintrat',
						'infpel_entrat_fecha_fintrat',
						'infpel_intrat',
						'infpel_intrat_diag',
						'infpel_intrat_reitrat',
						'infpel_intrat_fecha_reitrat',
						'fecha_creacion',
						'fecha_actualizacion',
						'relaciones_mismo_sexo',
						'dinero_por_relaciones',
						'identificacion_genero',
						'embarazada_vih',
						'fecha_ultima_menstruacion',
						'semanas_gestacion',
						'evaluacion_go',
						'programacion_cesaria',
						'fecha_cesaria',
						'afiliacion_seguridad_social',
						'clase_afiliacion',
						'seguro_privado',
						'nombre_aseguradora',
						'actualmente_tarv',
						'fecha_inicio_tarv',
						'estatus_actual_tarv',
						'fecha_diagnostico',
						'fecha_primera_consulta',
						'fecha_proxima_cita',
						'cita_medica',
						'retiro_medicamento',
						'talla',
						'peso',
						'imc',
					).filter(boleta=persona['id']).order_by('-fecha_actualizacion')[:1].get()
				)
						
			except Exception, e:
				clinica = False
				pass
		except Exception, e:
			clinica = False
			try:
				persona = dict(RPN.objects.values('primer_nombre', 'segundo_nombre', 'primer_apellido', 'segundo_apellido', 'sexo', 'fecha_nacimiento').get(identidad=identidad))
			except Exception, e:
				persona = False

		#VALIDACIONES DONDE SI TIENE BOLETA INGRESADA MAYOR DE 3
		# hoy = datetime.today().date()
		# try:
		# 	ultima_boleta = BoletasClinicas.objects.filter(boleta__identidad=identidad).order_by('-fecha_actualizacion')[:1].get()
		# 	fecha = add_months(ultima_boleta.fecha_actualizacion, 3)
		# 	if fecha > hoy:
		# 		persona = 'existe'
		# 		clinica = False
		# except Exception, e:
		# 	pass
		data ={
			'persona': persona,
			'clinica': clinica,
		}

		return HttpResponse(json.dumps(data, default=date_handler), content_type='application/json')
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
		if request.POST.get('identidad') == '' or request.POST.get('primer_nombre') == '' or request.POST.get('primer_apellido') == '':
			formulario = RPNForm(request.POST)
			formulario2 = BoletaForm(request.POST)
			formulario3 = BoletaClinicaForm(request.POST)
			ctx = {
				'formulario' : formulario,
				'formulario2': formulario2,
				'formulario3': formulario3,
				'embarazada': embarazada,
				'error': 'LOS DATOS GENERALES NO PUEDEN IR VACIOS, PORFAVOR REVISARLOS.',
				'responsable': responsable,
			}
			return render(request, 'boleta_clinica.html', ctx)

		ide = request.POST['identidad']
		identidad = ide.replace("-", "")
		#try:
		with transaction.atomic():
			tipo_persona = request.POST['persona']
	
			
			formulario = RPNForm(request.POST)
			formulario2 = BoletaForm(request.POST)
			formulario3 = BoletaClinicaForm(request.POST)
			if  formulario2.is_valid() and formulario3.is_valid():
				if str(tipo_persona) != '2':
					registro = formulario2.save(commit=False)
					registro.expediente =  identidad +'-'+ request.POST['fecha_nacimiento'] +'-'+ request.POST['sexo_persona']
					registro.grupo_etnico =  None if request.POST.get('grupo_etnico') == '' or request.POST.get('grupo_etnico') == None  else GruposEtnicos.objects.get(pk=request.POST.get('grupo_etnico'))
					try:
						registro.ciudad =  Ciudades.objects.get(pk=request.POST['ciudad'])
					except Exception, e:
						registro.ciudad =  None
					try:
						registro.municipio =  Municipios.objects.get(pk=request.POST['municipio'])
					except Exception, e:
						registro.municipio =  None
					registro.identidad =  identidad
					registro.sexo = request.POST['sexo_persona']
					registro.primer_nombre =  request.POST['primer_nombre']
					registro.segundo_nombre =  request.POST['segundo_nombre']
					registro.primer_apellido =  request.POST['primer_apellido']
					registro.segundo_apellido =  request.POST['segundo_apellido']
					registro.fecha_nacimiento =  request.POST['fecha_nacimiento']
					registro.identidad_madre = request.POST['identidad_madre'].replace("-", "")
					registro.identidad_padre = request.POST['identidad_padre'].replace("-", "")
					registro.identidad_tutor = request.POST['identidad_tutor'].replace("-", "")
					registro.rpn =  False
					registro.creado_por = request.user
					registro.actualizado_por = request.user
					registro.save()
					formulario2.save_m2m()
				else:
					#CON BOLETA
					instance = Boletas.objects.filter(identidad=identidad).order_by('-fecha_actualizacion')[:1].get()
					formulario2 = BoletaForm(request.POST, instance=instance)
					registro = formulario2.save(commit=False)
					registro.sexo = request.POST['sexo_persona']
					registro.expediente =  identidad +'-'+ request.POST['fecha_nacimiento'] +'-'+ request.POST['sexo_persona']
					registro.grupo_etnico =  None if request.POST.get('grupo_etnico') == '' or request.POST.get('grupo_etnico') == None else GruposEtnicos.objects.get(pk=request.POST.get('grupo_etnico'))
					try:
						registro.ciudad =  Ciudades.objects.get(pk=request.POST['ciudad'])
					except Exception, e:
						registro.ciudad =  None
					try:
						registro.municipio =  Municipios.objects.get(pk=request.POST['municipio'])
					except Exception, e:
						registro.municipio =  None
					registro.identidad_madre = request.POST['identidad_madre'].replace("-", "")
					registro.identidad_padre = request.POST['identidad_padre'].replace("-", "")
					registro.identidad_tutor = request.POST['identidad_tutor'].replace("-", "")
					registro.rpn =  True
					try:
						registro.ciudad =  Ciudades.objects.get(pk=request.POST['ciudad'])
					except Exception, e:
						pass

					registro.actualizado_por = request.user
					registro.save()
					formulario2.save_m2m()

				try:
					instance = BoletasClinicas.objects.get(pk=request.POST.get('boleta_clinica'))
					formulario3 = BoletaClinicaForm(request.POST, instance=instance)
				except Exception, e:
					formulario3 = BoletaClinicaForm(request.POST)

				registro2 = formulario3.save(commit=False)
				registro2.boleta = registro
				registro2.actualmente_tarv = request.POST.get('actualmente_tarv')
				if request.POST.get('fecha_inicio_tarv') != '':
					registro2.fecha_inicio_tarv = request.POST.get('fecha_inicio_tarv')
				else:
					registro2.fecha_inicio_tarv = None
				registro2.estatus_actual_tarv = request.POST.get('estatus_actual_tarv')
				registro2.estado_inmunologico = request.POST.get('estado_inmunologico')
				registro2.hepb_resultado = request.POST.get('hepb_resultado')
				registro2.hepc_resultado = request.POST.get('hepc_resultado')
				registro2.rpr_resultado = request.POST.get('rpr_resultado')
				registro2.estado_clinico= request.POST.get('estado_clinico')
				registro2.embarazada_vih= request.POST.get('embarazada_vih')
				registro2.evaluacion_go= request.POST.get('evaluacion_go')
				registro2.programacion_cesaria= request.POST.get('programacion_cesaria')
				registro2.afiliacion_seguridad_social= request.POST.get('afiliacion_seguridad_social')
				registro2.seguro_privado= request.POST.get('seguro_privado')
				registro2.relaciones_mismo_sexo= request.POST.get('relaciones_mismo_sexo')
				registro2.dinero_por_relaciones= request.POST.get('dinero_por_relaciones')
				registro2.identificacion_genero= request.POST.get('identificacion_genero')
				registro2.lic4= request.POST.get('lic4')
				registro2.lic4_ordenado_consulta= request.POST.get('lic4_ordenado_consulta')
				registro2.caviral= request.POST.get('caviral')
				registro2.caviral_ordenado_consulta= request.POST.get('caviral_ordenado_consulta')
				registro2.hepb= request.POST.get('hepb')
				registro2.hepb_ordenado_consulta= request.POST.get('hepb_ordenado_consulta')
				registro2.hepc= request.POST.get('hepc')
				registro2.hepc_ordenado_consulta= request.POST.get('hepc_ordenado_consulta')
				registro2.rpr= request.POST.get('rpr')
				registro2.rpr_ordenado_consulta= request.POST.get('rpr_ordenado_consulta')
				registro2.rxtorax= request.POST.get('rxtorax')
				registro2.rxtorax_ordenado_consulta= request.POST.get('rxtorax_ordenado_consulta')
				registro2.sespu= request.POST.get('sespu')
				registro2.sespu_ordenado_consulta= request.POST.get('sespu_ordenado_consulta')
				registro2.ppd= request.POST.get('ppd')
				registro2.ppd_ordenado_consulta= request.POST.get('ppd_ordenado_consulta')
				registro2.cultivo= request.POST.get('cultivo')
				registro2.cultivo_ordenado_consulta= request.POST.get('cultivo_ordenado_consulta')
				registro2.usg= request.POST.get('usg')
				registro2.usg_ordenado_consulta= request.POST.get('usg_ordenado_consulta')
				registro2.biopsia= request.POST.get('biopsia')
				registro2.biopsia_ordenado_consulta= request.POST.get('biopsia_ordenado_consulta')
				registro2.otro= request.POST.get('otro')
				registro2.otro_ordenado_consulta= request.POST.get('otro_ordenado_consulta')
				registro2.tupu= request.POST.get('tupu')
				registro2.tupu_initrat= request.POST.get('tupu_initrat')
				registro2.tupu_entrat= request.POST.get('tupu_entrat')
				registro2.tupu_entrat_fintrat= request.POST.get('tupu_entrat_fintrat')
				registro2.tupu_intrat= request.POST.get('tupu_intrat')
				registro2.tupu_intrat_reitrat= request.POST.get('tupu_intrat_reitrat')
				registro2.tupu_trat= request.POST.get('tupu_trat')
				registro2.tudi= request.POST.get('tudi')
				registro2.tudi_initrat= request.POST.get('tudi_initrat')
				registro2.tudi_entrat= request.POST.get('tudi_entrat')
				registro2.tudi_entrat_fintrat= request.POST.get('tudi_entrat_fintrat')
				registro2.tudi_intrat= request.POST.get('tudi_intrat')
				registro2.tudi_intrat_reitrat= request.POST.get('tudi_intrat_reitrat')
				registro2.tudi_trat= request.POST.get('tudi_trat')
				registro2.hepb= request.POST.get('hepb')
				registro2.hepb_initrat= request.POST.get('hepb_initrat')
				registro2.hepb_entrat= request.POST.get('hepb_entrat')
				registro2.hepb_entrat_fintrat= request.POST.get('hepb_entrat_fintrat')
				registro2.hepb_intrat= request.POST.get('hepb_intrat')
				registro2.hepb_intrat_reitrat= request.POST.get('hepb_intrat_reitrat')
				registro2.hepb_trat= request.POST.get('hepb_trat')
				registro2.hepc= request.POST.get('hepc')
				registro2.hepc_initrat= request.POST.get('hepc_initrat')
				registro2.hepc_entrat= request.POST.get('hepc_entrat')
				registro2.hepc_entrat_fintrat= request.POST.get('hepc_entrat_fintrat')
				registro2.hepc_intrat= request.POST.get('hepc_intrat')
				registro2.hepc_intrat_reitrat= request.POST.get('hepc_intrat_reitrat')
				registro2.hepc_trat= request.POST.get('hepc_trat')
				registro2.ulg= request.POST.get('ulg')
				registro2.ulg_initrat= request.POST.get('ulg_initrat')
				registro2.ulg_entrat= request.POST.get('ulg_entrat')
				registro2.ulg_entrat_fintrat= request.POST.get('ulg_entrat_fintrat')
				registro2.ulg_intrat= request.POST.get('ulg_intrat')
				registro2.ulg_intrat_reitrat= request.POST.get('ulg_intrat_reitrat')
				registro2.ulg_trat= request.POST.get('ulg_trat')
				registro2.secure= request.POST.get('secure')
				registro2.secure_initrat= request.POST.get('secure_initrat')
				registro2.secure_entrat= request.POST.get('secure_entrat')
				registro2.secure_entrat_fintrat= request.POST.get('secure_entrat_fintrat')
				registro2.secure_intrat= request.POST.get('secure_intrat')
				registro2.secure_intrat_reitrat= request.POST.get('secure_intrat_reitrat')
				registro2.secure_trat= request.POST.get('secure_trat')
				registro2.fluva= request.POST.get('fluva')
				registro2.fluva_initrat= request.POST.get('fluva_initrat')
				registro2.fluva_entrat= request.POST.get('fluva_entrat')
				registro2.fluva_entrat_fintrat= request.POST.get('fluva_entrat_fintrat')
				registro2.fluva_intrat= request.POST.get('fluva_intrat')
				registro2.fluva_intrat_reitrat= request.POST.get('fluva_intrat_reitrat')
				registro2.fluva_trat= request.POST.get('fluva_trat')
				registro2.buin= request.POST.get('buin')
				registro2.buin_initrat= request.POST.get('buin_initrat')
				registro2.buin_entrat= request.POST.get('buin_entrat')
				registro2.buin_entrat_fintrat= request.POST.get('buin_entrat_fintrat')
				registro2.buin_intrat= request.POST.get('buin_intrat')
				registro2.buin_intrat_reitrat= request.POST.get('buin_intrat_reitrat')
				registro2.buin_trat= request.POST.get('buin_trat')
				registro2.edes= request.POST.get('edes')
				registro2.edes_initrat= request.POST.get('edes_initrat')
				registro2.edes_entrat= request.POST.get('edes_entrat')
				registro2.edes_entrat_fintrat= request.POST.get('edes_entrat_fintrat')
				registro2.edes_intrat= request.POST.get('edes_intrat')
				registro2.edes_intrat_reitrat= request.POST.get('edes_intrat_reitrat')
				registro2.edes_trat= request.POST.get('edes_trat')
				registro2.verge= request.POST.get('verge')
				registro2.verge_initrat= request.POST.get('verge_initrat')
				registro2.verge_entrat= request.POST.get('verge_entrat')
				registro2.verge_entrat_fintrat= request.POST.get('verge_entrat_fintrat')
				registro2.verge_intrat= request.POST.get('verge_intrat')
				registro2.verge_intrat_reitrat= request.POST.get('verge_intrat_reitrat')
				registro2.verge_trat= request.POST.get('verge_trat')
				registro2.trasex= request.POST.get('trasex')
				registro2.trasex_initrat= request.POST.get('trasex_initrat')
				registro2.trasex_entrat= request.POST.get('trasex_entrat')
				registro2.trasex_entrat_fintrat= request.POST.get('trasex_entrat_fintrat')
				registro2.trasex_intrat= request.POST.get('trasex_intrat')
				registro2.trasex_intrat_reitrat= request.POST.get('trasex_intrat_reitrat')
				registro2.trasex_trat= request.POST.get('trasex_trat')
				registro2.proc= request.POST.get('proc')
				registro2.proc_initrat= request.POST.get('proc_initrat')
				registro2.proc_entrat= request.POST.get('proc_entrat')
				registro2.proc_entrat_fintrat= request.POST.get('proc_entrat_fintrat')
				registro2.proc_intrat= request.POST.get('proc_intrat')
				registro2.proc_intrat_reitrat= request.POST.get('proc_intrat_reitrat')
				registro2.proc_trat= request.POST.get('proc_trat')
				registro2.infpel= request.POST.get('infpel')
				registro2.infpel_initrat= request.POST.get('infpel_initrat')
				registro2.infpel_entrat= request.POST.get('infpel_entrat')
				registro2.infpel_entrat_fintrat= request.POST.get('infpel_entrat_fintrat')
				registro2.infpel_intrat= request.POST.get('infpel_intrat')
				registro2.infpel_intrat_reitrat= request.POST.get('infpel_intrat_reitrat')
				registro2.infpel_trat= request.POST.get('infpel_trat')
				registro2.actualizado_por = request.user
				if request.POST.get('fecha_ultima_menstruacion') != '':
					registro2.fecha_ultima_menstruacion = request.POST.get('fecha_ultima_menstruacion')
				else:
					registro2.fecha_ultima_menstruacion = None
				if request.POST.get('fecha_cesaria') != '':
					registro2.fecha_cesaria = request.POST.get('fecha_cesaria')
				else:
					registro2.fecha_cesaria = None
				if request.POST.get('fecha_inicio_tarv') != '':
					registro2.fecha_inicio_tarv = request.POST.get('fecha_inicio_tarv')
				else:
					registro2.fecha_inicio_tarv = None
				if request.POST.get('fecha_diagnostico') != '':
					registro2.fecha_diagnostico = request.POST.get('fecha_diagnostico')
				else:
					registro2.fecha_diagnostico = None
				if request.POST.get('fecha_primera_consulta') != '':
					registro2.fecha_primera_consulta = request.POST.get('fecha_primera_consulta')
				else:
					registro2.fecha_primera_consulta = None
				if request.POST.get('fecha_proxima_cita') != '':
					registro2.fecha_proxima_cita = request.POST.get('fecha_proxima_cita')
				else:
					registro2.fecha_proxima_cita = None
				if request.POST.get('lic4_fecha_realizacion') != '':
					registro2.lic4_fecha_realizacion = request.POST.get('lic4_fecha_realizacion')
				else:
					registro2.lic4_fecha_realizacion = None
				if request.POST.get('caviral_fecha_realizacion') != '':
					registro2.caviral_fecha_realizacion = request.POST.get('caviral_fecha_realizacion')
				else:
					registro2.caviral_fecha_realizacion = None
				if request.POST.get('hepb_fecha_realizacion') != '':
					registro2.hepb_fecha_realizacion = request.POST.get('hepb_fecha_realizacion')
				else:
					registro2.hepb_fecha_realizacion = None
				if request.POST.get('hepc_fecha_realizacion') != '':
					registro2.hepc_fecha_realizacion = request.POST.get('hepc_fecha_realizacion')
				else:
					registro2.hepc_fecha_realizacion = None
				if request.POST.get('rpr_fecha_realizacion') != '':
					registro2.rpr_fecha_realizacion = request.POST.get('rpr_fecha_realizacion')
				else:
					registro2.rpr_fecha_realizacion = None
				if request.POST.get('rxtorax_fecha_realizacion') != '':
					registro2.rxtorax_fecha_realizacion = request.POST.get('rxtorax_fecha_realizacion')
				else:
					registro2.rxtorax_fecha_realizacion = None
				if request.POST.get('sespu_fecha_realizacion') != '':
					registro2.sespu_fecha_realizacion = request.POST.get('sespu_fecha_realizacion')
				else:
					registro2.sespu_fecha_realizacion = None
				if request.POST.get('ppd_fecha_realizacion') != '':
					registro2.ppd_fecha_realizacion = request.POST.get('ppd_fecha_realizacion')
				else:
					registro2.ppd_fecha_realizacion = None
				if request.POST.get('cultivo_fecha_realizacion') != '':
					registro2.cultivo_fecha_realizacion = request.POST.get('cultivo_fecha_realizacion')
				else:
					registro2.cultivo_fecha_realizacion = None
				if request.POST.get('usg_fecha_realizacion') != '':
					registro2.usg_fecha_realizacion = request.POST.get('usg_fecha_realizacion')
				else:
					registro2.usg_fecha_realizacion = None
				if request.POST.get('biopsia_fecha_realizacion') != '':
					registro2.biopsia_fecha_realizacion = request.POST.get('biopsia_fecha_realizacion')
				else:
					registro2.biopsia_fecha_realizacion = None
				if request.POST.get('otro_fecha_realizacion') != '':
					registro2.otro_fecha_realizacion = request.POST.get('otro_fecha_realizacion')
				else:
					registro2.otro_fecha_realizacion = None
				if request.POST.get('tupu_diag') != '':
					registro2.tupu_diag = request.POST.get('tupu_diag')
				else:
					registro2.tupu_diag = None
				if request.POST.get('tupu_fecha_initrat') != '':
					registro2.tupu_fecha_initrat = request.POST.get('tupu_fecha_initrat')
				else:
					registro2.tupu_fecha_initrat = None
				if request.POST.get('tupu_entrat_diag') != '':
					registro2.tupu_entrat_diag = request.POST.get('tupu_entrat_diag')
				else:
					registro2.tupu_entrat_diag = None
				if request.POST.get('tupu_entrat_fecha_fintrat') != '':
					registro2.tupu_entrat_fecha_fintrat = request.POST.get('tupu_entrat_fecha_fintrat')
				else:
					registro2.tupu_entrat_fecha_fintrat = None
				if request.POST.get('tupu_intrat_diag') != '':
					registro2.tupu_intrat_diag = request.POST.get('tupu_intrat_diag')
				else:
					registro2.tupu_intrat_diag = None
				if request.POST.get('tupu_intrat_fecha_reitrat') != '':
					registro2.tupu_intrat_fecha_reitrat = request.POST.get('tupu_intrat_fecha_reitrat')
				else:
					registro2.tupu_intrat_fecha_reitrat = None
				if request.POST.get('tudi_diag') != '':
					registro2.tudi_diag = request.POST.get('tudi_diag')
				else:
					registro2.tudi_diag = None
				if request.POST.get('tudi_fecha_initrat') != '':
					registro2.tudi_fecha_initrat = request.POST.get('tudi_fecha_initrat')
				else:
					registro2.tudi_fecha_initrat = None
				if request.POST.get('tudi_entrat_diag') != '':
					registro2.tudi_entrat_diag = request.POST.get('tudi_entrat_diag')
				else:
					registro2.tudi_entrat_diag = None
				if request.POST.get('tudi_entrat_fecha_fintrat') != '':
					registro2.tudi_entrat_fecha_fintrat = request.POST.get('tudi_entrat_fecha_fintrat')
				else:
					registro2.tudi_entrat_fecha_fintrat = None
				if request.POST.get('tudi_intrat_diag') != '':
					registro2.tudi_intrat_diag = request.POST.get('tudi_intrat_diag')
				else:
					registro2.tudi_intrat_diag = None
				if request.POST.get('tudi_intrat_fecha_reitrat') != '':
					registro2.tudi_intrat_fecha_reitrat = request.POST.get('tudi_intrat_fecha_reitrat')
				else:
					registro2.tudi_intrat_fecha_reitrat = None
				if request.POST.get('hepb_diag') != '':
					registro2.hepb_diag = request.POST.get('hepb_diag')
				else:
					registro2.hepb_diag = None
				if request.POST.get('hepb_fecha_initrat') != '':
					registro2.hepb_fecha_initrat = request.POST.get('hepb_fecha_initrat')
				else:
					registro2.hepb_fecha_initrat = None
				if request.POST.get('hepb_entrat_diag') != '':
					registro2.hepb_entrat_diag = request.POST.get('hepb_entrat_diag')
				else:
					registro2.hepb_entrat_diag = None
				if request.POST.get('hepb_entrat_fecha_fintrat') != '':
					registro2.hepb_entrat_fecha_fintrat = request.POST.get('hepb_entrat_fecha_fintrat')
				else:
					registro2.hepb_entrat_fecha_fintrat = None
				if request.POST.get('hepb_intrat_diag') != '':
					registro2.hepb_intrat_diag = request.POST.get('hepb_intrat_diag')
				else:
					registro2.hepb_intrat_diag = None
				if request.POST.get('hepb_intrat_fecha_reitrat') != '':
					registro2.hepb_intrat_fecha_reitrat = request.POST.get('hepb_intrat_fecha_reitrat')
				else:
					registro2.hepb_intrat_fecha_reitrat = None
				if request.POST.get('hepc_diag') != '':
					registro2.hepc_diag = request.POST.get('hepc_diag')
				else:
					registro2.hepc_diag = None
				if request.POST.get('hepc_fecha_initrat') != '':
					registro2.hepc_fecha_initrat = request.POST.get('hepc_fecha_initrat')
				else:
					registro2.hepc_fecha_initrat = None
				if request.POST.get('hepc_entrat_diag') != '':
					registro2.hepc_entrat_diag = request.POST.get('hepc_entrat_diag')
				else:
					registro2.hepc_entrat_diag = None
				if request.POST.get('hepc_entrat_fecha_fintrat') != '':
					registro2.hepc_entrat_fecha_fintrat = request.POST.get('hepc_entrat_fecha_fintrat')
				else:
					registro2.hepc_entrat_fecha_fintrat = None
				if request.POST.get('hepc_intrat_diag') != '':
					registro2.hepc_intrat_diag = request.POST.get('hepc_intrat_diag')
				else:
					registro2.hepc_intrat_diag = None
				if request.POST.get('hepc_intrat_fecha_reitrat') != '':
					registro2.hepc_intrat_fecha_reitrat = request.POST.get('hepc_intrat_fecha_reitrat')
				else:
					registro2.hepc_intrat_fecha_reitrat = None
				if request.POST.get('ulg_diag') != '':
					registro2.ulg_diag = request.POST.get('ulg_diag')
				else:
					registro2.ulg_diag = None
				if request.POST.get('ulg_fecha_initrat') != '':
					registro2.ulg_fecha_initrat = request.POST.get('ulg_fecha_initrat')
				else:
					registro2.ulg_fecha_initrat = None
				if request.POST.get('ulg_entrat_diag') != '':
					registro2.ulg_entrat_diag = request.POST.get('ulg_entrat_diag')
				else:
					registro2.ulg_entrat_diag = None
				if request.POST.get('ulg_entrat_fecha_fintrat') != '':
					registro2.ulg_entrat_fecha_fintrat = request.POST.get('ulg_entrat_fecha_fintrat')
				else:
					registro2.ulg_entrat_fecha_fintrat = None
				if request.POST.get('ulg_intrat_diag') != '':
					registro2.ulg_intrat_diag = request.POST.get('ulg_intrat_diag')
				else:
					registro2.ulg_intrat_diag = None
				if request.POST.get('ulg_intrat_fecha_reitrat') != '':
					registro2.ulg_intrat_fecha_reitrat = request.POST.get('ulg_intrat_fecha_reitrat')
				else:
					registro2.ulg_intrat_fecha_reitrat = None
				if request.POST.get('secure_diag') != '':
					registro2.secure_diag = request.POST.get('secure_diag')
				else:
					registro2.secure_diag = None
				if request.POST.get('secure_fecha_initrat') != '':
					registro2.secure_fecha_initrat = request.POST.get('secure_fecha_initrat')
				else:
					registro2.secure_fecha_initrat = None
				if request.POST.get('secure_entrat_diag') != '':
					registro2.secure_entrat_diag = request.POST.get('secure_entrat_diag')
				else:
					registro2.secure_entrat_diag = None
				if request.POST.get('secure_entrat_fecha_fintrat') != '':
					registro2.secure_entrat_fecha_fintrat = request.POST.get('secure_entrat_fecha_fintrat')
				else:
					registro2.secure_entrat_fecha_fintrat = None
				if request.POST.get('secure_intrat_diag') != '':
					registro2.secure_intrat_diag = request.POST.get('secure_intrat_diag')
				else:
					registro2.secure_intrat_diag = None
				if request.POST.get('secure_intrat_fecha_reitrat') != '':
					registro2.secure_intrat_fecha_reitrat = request.POST.get('secure_intrat_fecha_reitrat')
				else:
					registro2.secure_intrat_fecha_reitrat = None
				if request.POST.get('fluva_diag') != '':
					registro2.fluva_diag = request.POST.get('fluva_diag')
				else:
					registro2.fluva_diag = None
				if request.POST.get('fluva_fecha_initrat') != '':
					registro2.fluva_fecha_initrat = request.POST.get('fluva_fecha_initrat')
				else:
					registro2.fluva_fecha_initrat = None
				if request.POST.get('fluva_entrat_diag') != '':
					registro2.fluva_entrat_diag = request.POST.get('fluva_entrat_diag')
				else:
					registro2.fluva_entrat_diag = None
				if request.POST.get('fluva_entrat_fecha_fintrat') != '':
					registro2.fluva_entrat_fecha_fintrat = request.POST.get('fluva_entrat_fecha_fintrat')
				else:
					registro2.fluva_entrat_fecha_fintrat = None
				if request.POST.get('fluva_intrat_diag') != '':
					registro2.fluva_intrat_diag = request.POST.get('fluva_intrat_diag')
				else:
					registro2.fluva_intrat_diag = None
				if request.POST.get('fluva_intrat_fecha_reitrat') != '':
					registro2.fluva_intrat_fecha_reitrat = request.POST.get('fluva_intrat_fecha_reitrat')
				else:
					registro2.fluva_intrat_fecha_reitrat = None
				if request.POST.get('buin_diag') != '':
					registro2.buin_diag = request.POST.get('buin_diag')
				else:
					registro2.buin_diag = None
				if request.POST.get('buin_fecha_initrat') != '':
					registro2.buin_fecha_initrat = request.POST.get('buin_fecha_initrat')
				else:
					registro2.buin_fecha_initrat = None
				if request.POST.get('buin_entrat_diag') != '':
					registro2.buin_entrat_diag = request.POST.get('buin_entrat_diag')
				else:
					registro2.buin_entrat_diag = None
				if request.POST.get('buin_entrat_fecha_fintrat') != '':
					registro2.buin_entrat_fecha_fintrat = request.POST.get('buin_entrat_fecha_fintrat')
				else:
					registro2.buin_entrat_fecha_fintrat = None
				if request.POST.get('buin_intrat_diag') != '':
					registro2.buin_intrat_diag = request.POST.get('buin_intrat_diag')
				else:
					registro2.buin_intrat_diag = None
				if request.POST.get('buin_intrat_fecha_reitrat') != '':
					registro2.buin_intrat_fecha_reitrat = request.POST.get('buin_intrat_fecha_reitrat')
				else:
					registro2.buin_intrat_fecha_reitrat = None
				if request.POST.get('edes_diag') != '':
					registro2.edes_diag = request.POST.get('edes_diag')
				else:
					registro2.edes_diag = None
				if request.POST.get('edes_fecha_initrat') != '':
					registro2.edes_fecha_initrat = request.POST.get('edes_fecha_initrat')
				else:
					registro2.edes_fecha_initrat = None
				if request.POST.get('edes_entrat_diag') != '':
					registro2.edes_entrat_diag = request.POST.get('edes_entrat_diag')
				else:
					registro2.edes_entrat_diag = None
				if request.POST.get('edes_entrat_fecha_fintrat') != '':
					registro2.edes_entrat_fecha_fintrat = request.POST.get('edes_entrat_fecha_fintrat')
				else:
					registro2.edes_entrat_fecha_fintrat = None
				if request.POST.get('edes_intrat_diag') != '':
					registro2.edes_intrat_diag = request.POST.get('edes_intrat_diag')
				else:
					registro2.edes_intrat_diag = None
				if request.POST.get('edes_intrat_fecha_reitrat') != '':
					registro2.edes_intrat_fecha_reitrat = request.POST.get('edes_intrat_fecha_reitrat')
				else:
					registro2.edes_intrat_fecha_reitrat = None
				if request.POST.get('verge_diag') != '':
					registro2.verge_diag = request.POST.get('verge_diag')
				else:
					registro2.verge_diag = None
				if request.POST.get('verge_fecha_initrat') != '':
					registro2.verge_fecha_initrat = request.POST.get('verge_fecha_initrat')
				else:
					registro2.verge_fecha_initrat = None
				if request.POST.get('verge_entrat_diag') != '':
					registro2.verge_entrat_diag = request.POST.get('verge_entrat_diag')
				else:
					registro2.verge_entrat_diag = None
				if request.POST.get('verge_entrat_fecha_fintrat') != '':
					registro2.verge_entrat_fecha_fintrat = request.POST.get('verge_entrat_fecha_fintrat')
				else:
					registro2.verge_entrat_fecha_fintrat = None
				if request.POST.get('verge_intrat_diag') != '':
					registro2.verge_intrat_diag = request.POST.get('verge_intrat_diag')
				else:
					registro2.verge_intrat_diag = None
				if request.POST.get('verge_intrat_fecha_reitrat') != '':
					registro2.verge_intrat_fecha_reitrat = request.POST.get('verge_intrat_fecha_reitrat')
				else:
					registro2.verge_intrat_fecha_reitrat = None
				if request.POST.get('trasex_diag') != '':
					registro2.trasex_diag = request.POST.get('trasex_diag')
				else:
					registro2.trasex_diag = None
				if request.POST.get('trasex_fecha_initrat') != '':
					registro2.trasex_fecha_initrat = request.POST.get('trasex_fecha_initrat')
				else:
					registro2.trasex_fecha_initrat = None
				if request.POST.get('trasex_entrat_diag') != '':
					registro2.trasex_entrat_diag = request.POST.get('trasex_entrat_diag')
				else:
					registro2.trasex_entrat_diag = None
				if request.POST.get('trasex_entrat_fecha_fintrat') != '':
					registro2.trasex_entrat_fecha_fintrat = request.POST.get('trasex_entrat_fecha_fintrat')
				else:
					registro2.trasex_entrat_fecha_fintrat = None
				if request.POST.get('trasex_intrat_diag') != '':
					registro2.trasex_intrat_diag = request.POST.get('trasex_intrat_diag')
				else:
					registro2.trasex_intrat_diag = None
				if request.POST.get('trasex_intrat_fecha_reitrat') != '':
					registro2.trasex_intrat_fecha_reitrat = request.POST.get('trasex_intrat_fecha_reitrat')
				else:
					registro2.trasex_intrat_fecha_reitrat = None
				if request.POST.get('proc_diag') != '':
					registro2.proc_diag = request.POST.get('proc_diag')
				else:
					registro2.proc_diag = None
				if request.POST.get('proc_fecha_initrat') != '':
					registro2.proc_fecha_initrat = request.POST.get('proc_fecha_initrat')
				else:
					registro2.proc_fecha_initrat = None
				if request.POST.get('proc_entrat_diag') != '':
					registro2.proc_entrat_diag = request.POST.get('proc_entrat_diag')
				else:
					registro2.proc_entrat_diag = None
				if request.POST.get('proc_entrat_fecha_fintrat') != '':
					registro2.proc_entrat_fecha_fintrat = request.POST.get('proc_entrat_fecha_fintrat')
				else:
					registro2.proc_entrat_fecha_fintrat = None
				if request.POST.get('proc_intrat_diag') != '':
					registro2.proc_intrat_diag = request.POST.get('proc_intrat_diag')
				else:
					registro2.proc_intrat_diag = None
				if request.POST.get('proc_intrat_fecha_reitrat') != '':
					registro2.proc_intrat_fecha_reitrat = request.POST.get('proc_intrat_fecha_reitrat')
				else:
					registro2.proc_intrat_fecha_reitrat = None
				if request.POST.get('infpel_diag') != '':
					registro2.infpel_diag = request.POST.get('infpel_diag')
				else:
					registro2.infpel_diag = None
				if request.POST.get('infpel_fecha_initrat') != '':
					registro2.infpel_fecha_initrat = request.POST.get('infpel_fecha_initrat')
				else:
					registro2.infpel_fecha_initrat = None
				if request.POST.get('infpel_entrat_diag') != '':
					registro2.infpel_entrat_diag = request.POST.get('infpel_entrat_diag')
				else:
					registro2.infpel_entrat_diag = None
				if request.POST.get('infpel_entrat_fecha_fintrat') != '':
					registro2.infpel_entrat_fecha_fintrat = request.POST.get('infpel_entrat_fecha_fintrat')
				else:
					registro2.infpel_entrat_fecha_fintrat = None
				if request.POST.get('infpel_intrat_diag') != '':
					registro2.infpel_intrat_diag = request.POST.get('infpel_intrat_diag')
				else:
					registro2.infpel_intrat_diag = None
				if request.POST.get('infpel_intrat_fecha_reitrat') != '':	
					registro2.infpel_intrat_fecha_reitrat = request.POST.get('infpel_intrat_fecha_reitrat')
				else:
					registro2.infpel_intrat_fecha_reitrat = None
				registro2.creado_por = request.user
				try:
					responsable = Responsables.objects.get(usuario_sistema=request.user)
					registro2.establecimiento = responsable.establecimiento
				except Exception, e:
					registro2.establecimiento = None

				registro2.save()

				formulario = RPNForm()
				formulario.fields['sexo'].widget.attrs['disabled'] = True

				formulario2 = BoletaForm()
				formulario3 = BoletaClinicaForm()
				exito = True

			else:
				pass
		#except Exception, e:
		#	raise e
		#	print 'ERROR', e
		ctx = {
			'formulario' : formulario,
			'formulario2' : formulario2,
			'formulario3' : formulario3,
			'exito': exito,
			'responsable': responsable,
			'embarazada': embarazada,
		}
		return render(request, 'boleta_clinica.html', ctx)




@transaction.atomic
@login_required()
def boleta_seguimiento(request):
	try:
		responsable = usuario(request.user.pk)
	except Exception, e:
		responsable = ''

	try:
		embarazada = Condiciones.objects.get(nombre='Embarazada')
	except Exception, e:
		embarazada = ''
	exito = False
	#AJAX
	if request.is_ajax():
		identidad = request.GET['identidad']
		try:
			persona = dict(
				BoletasClinicas.objects.values(
					'id',
					'boleta__identidad', 
					'boleta__primer_nombre', 
					'boleta__segundo_nombre', 
					'boleta__primer_apellido', 
					'boleta__segundo_apellido', 
					'boleta__sexo', 
					'boleta__fecha_nacimiento',
					'boleta__edad_anios',
					'boleta__edad_meses',
					'boleta__edad_dias',
					'estado_inmunologico',
					'estado_clinico',
					'estadio_infeccion',
					'lic4',
					'lic4_resultado',
					'lic4_fecha_realizacion',
					'lic4_ordenado_consulta',
					'caviral',
					'caviral_resultado',
					'caviral_fecha_realizacion',
					'caviral_ordenado_consulta',
					'hepb',
					'hepb_resultado',
					'hepb_fecha_realizacion',
					'hepb_ordenado_consulta',
					'hepc',
					'hepc_resultado',
					'hepc_fecha_realizacion',
					'hepc_ordenado_consulta',
					'rpr',
					'rpr_resultado',
					'rpr_fecha_realizacion',
					'rpr_ordenado_consulta',
					'rxtorax',
					'rxtorax_resultado',
					'rxtorax_fecha_realizacion',
					'rxtorax_ordenado_consulta',
					'sespu',
					'sespu_resultado',
					'sespu_fecha_realizacion',
					'sespu_ordenado_consulta',
					'ppd',
					'ppd_resultado',
					'ppd_fecha_realizacion',
					'ppd_ordenado_consulta',
					'cultivo',
					'cultivo_resultado',
					'cultivo_fecha_realizacion',
					'cultivo_ordenado_consulta',
					'usg',
					'usg_resultado',
					'usg_fecha_realizacion',
					'usg_ordenado_consulta',
					'biopsia',
					'biopsia_resultado',
					'biopsia_fecha_realizacion',
					'biopsia_ordenado_consulta',
					'otro',
					'otro_resultado',
					'otro_fecha_realizacion',
					'otro_ordenado_consulta',
					'tupu',
					'tupu_diag',
					'tupu_initrat',
					'tupu_fecha_initrat',
					'tupu_entrat',
					'tupu_entrat_diag',
					'tupu_entrat_fintrat',
					'tupu_entrat_fecha_fintrat',
					'tupu_intrat',
					'tupu_intrat_diag',
					'tupu_intrat_reitrat',
					'tupu_intrat_fecha_reitrat',
					'tupu_trat',
					'tudi',
					'tudi_diag',
					'tudi_initrat',
					'tudi_fecha_initrat',
					'tudi_entrat',
					'tudi_entrat_diag',
					'tudi_entrat_fintrat',
					'tudi_entrat_fecha_fintrat',
					'tudi_intrat',
					'tudi_intrat_diag',
					'tudi_intrat_reitrat',
					'tudi_intrat_fecha_reitrat',
					'hepb',
					'hepb_diag',
					'hepb_initrat',
					'hepb_fecha_initrat',
					'hepb_entrat',
					'hepb_entrat_diag',
					'hepb_entrat_fintrat',
					'hepb_entrat_fecha_fintrat',
					'hepb_intrat',
					'hepb_intrat_diag',
					'hepb_intrat_reitrat',
					'hepb_intrat_fecha_reitrat',
					'hepc',
					'hepc_diag',
					'hepc_initrat',
					'hepc_fecha_initrat',
					'hepc_entrat',
					'hepc_entrat_diag',
					'hepc_entrat_fintrat',
					'hepc_entrat_fecha_fintrat',
					'hepc_intrat',
					'hepc_intrat_diag',
					'hepc_intrat_reitrat',
					'hepc_intrat_fecha_reitrat',
					'ulg',
					'ulg_diag',
					'ulg_initrat',
					'ulg_fecha_initrat',
					'ulg_entrat',
					'ulg_entrat_diag',
					'ulg_entrat_fintrat',
					'ulg_entrat_fecha_fintrat',
					'ulg_intrat',
					'ulg_intrat_diag',
					'ulg_intrat_reitrat',
					'ulg_intrat_fecha_reitrat',
					'secure',
					'secure_diag',
					'secure_initrat',
					'secure_fecha_initrat',
					'secure_entrat',
					'secure_entrat_diag',
					'secure_entrat_fintrat',
					'secure_entrat_fecha_fintrat',
					'secure_intrat',
					'secure_intrat_diag',
					'secure_intrat_reitrat',
					'secure_intrat_fecha_reitrat',
					'fluva',
					'fluva_diag',
					'fluva_initrat',
					'fluva_fecha_initrat',
					'fluva_entrat',
					'fluva_entrat_diag',
					'fluva_entrat_fintrat',
					'fluva_entrat_fecha_fintrat',
					'fluva_intrat',
					'fluva_intrat_diag',
					'fluva_intrat_reitrat',
					'fluva_intrat_fecha_reitrat',
					'buin',
					'buin_diag',
					'buin_initrat',
					'buin_fecha_initrat',
					'buin_entrat',
					'buin_entrat_diag',
					'buin_entrat_fintrat',
					'buin_entrat_fecha_fintrat',
					'buin_intrat',
					'buin_intrat_diag',
					'buin_intrat_reitrat',
					'buin_intrat_fecha_reitrat',
					'edes',
					'edes_diag',
					'edes_initrat',
					'edes_fecha_initrat',
					'edes_entrat',
					'edes_entrat_diag',
					'edes_entrat_fintrat',
					'edes_entrat_fecha_fintrat',
					'edes_intrat',
					'edes_intrat_diag',
					'edes_intrat_reitrat',
					'edes_intrat_fecha_reitrat',
					'verge',
					'verge_diag',
					'verge_initrat',
					'verge_fecha_initrat',
					'verge_entrat',
					'verge_entrat_diag',
					'verge_entrat_fintrat',
					'verge_entrat_fecha_fintrat',
					'verge_intrat',
					'verge_intrat_diag',
					'verge_intrat_reitrat',
					'verge_intrat_fecha_reitrat',
					'trasex',
					'trasex_diag',
					'trasex_initrat',
					'trasex_fecha_initrat',
					'trasex_entrat',
					'trasex_entrat_diag',
					'trasex_entrat_fintrat',
					'trasex_entrat_fecha_fintrat',
					'trasex_intrat',
					'trasex_intrat_diag',
					'trasex_intrat_reitrat',
					'trasex_intrat_fecha_reitrat',
					'proc',
					'proc_diag',
					'proc_initrat',
					'proc_fecha_initrat',
					'proc_entrat',
					'proc_entrat_diag',
					'proc_entrat_fintrat',
					'proc_entrat_fecha_fintrat',
					'proc_intrat',
					'proc_intrat_diag',
					'proc_intrat_reitrat',
					'proc_intrat_fecha_reitrat',
					'infpel',
					'infpel_diag',
					'infpel_initrat',
					'infpel_fecha_initrat',
					'infpel_entrat',
					'infpel_entrat_diag',
					'infpel_entrat_fintrat',
					'infpel_entrat_fecha_fintrat',
					'infpel_intrat',
					'infpel_intrat_diag',
					'infpel_intrat_reitrat',
					'infpel_intrat_fecha_reitrat',
					'fecha_creacion',
					'fecha_actualizacion',
					
				).filter(boleta__identidad=identidad).order_by('-fecha_actualizacion')[:1].get()
			)
			try:
				seguimiento = dict(
					BoletasSeguimientos.objects.values(
						'id',
						'motivo',
						'profpri',
						'fecha_consulta',
						'fecha_proxima_cita',
						'tmpsmx',
						'tmpsmx_initrat',
						'tmpsmx_fecha_initrat',
						'tmpsmx_fintrat',
						'tmpsmx_fecha_fintrat',
						'tmpsmx_intrat',
						'tmpsmx_fecha_intrat',
						'tmpsmx_reitrat',
						'tmpsmx_fecha_reitrat',
						'isoniacida',
						'isoniacida_initrat',
						'isoniacida_fecha_initrat',
						'isoniacida_fintrat',
						'isoniacida_fecha_fintrat',
						'isoniacida_intrat',
						'isoniacida_fecha_intrat',
						'isoniacida_reitrat',
						'isoniacida_fecha_reitrat',
						'azitromicida',
						'azitromicida_initrat',
						'azitromicida_fecha_initrat',
						'azitromicida_fintrat',
						'azitromicida_fecha_fintrat',
						'azitromicida_intrat',
						'azitromicida_fecha_intrat',
						'azitromicida_reitrat',
						'azitromicida_fecha_reitrat',
						'arv_fecha_ini',
						'conteo_cd4',
						'abandono',
						'fecha_abandono',
						'suspension',
						'fecha_suspension',
						'fecha_reinicio',
						'fallecido',
						'fecha_fallecido',
						'causa_fallecido',
						'activo',
						'esquema_arv',
						'fecha_prescripcion_arv',
						'cambio_terapia',
						'fecha_cambio_terapia',
						'motivo_cambio_terapia',
						'documentado_con',
						'esquema_actual_arv',
						'fecha_entrega_arv',
						'azt',
						'abc',
						'efv',
						'rpv',
						'dtf',
						'lpv',
						'abc_cant',
						'ft_cant',
						'd4t_cant',
						'azt_cant',
						'efv_cant',
						'nvp_cant',
						'ddi_cant',
						'tc_cant',
						'tdf_cant',
						'rpv_cant',
						'etr_cant',
						'atv_cant',
						'drv_cant',
						'fpv_cant',
						'idv_cant',
						'nfv_cant',
						'sqv_cant',
						'tpv_cant',
						'ral_cant',
						'evg_cant',
						'dtg_cant',
						'abc_med',
						'ft_med',
						'd4t_med',
						'azt_med',
						'efv_med',
						'nvp_med',
						'ddi_med',
						'tc_med',
						'tdf_med',
						'rpv_med',
						'etr_med',
						'atv_med',
						'drv_med',
						'fpv_med',
						'idv_med',
						'nfv_med',
						'sqv_med',
						'tpv_med',
						'ral_med',
						'evg_med',
						'dtg_med',
						'abc_ter',
						'ft_ter',
						'd4t_ter',
						'azt_ter',
						'efv_ter',
						'nvp_ter',
						'ddi_ter',
						'tc_ter',
						'tdf_ter',
						'rpv_ter',
						'etr_ter',
						'atv_ter',
						'drv_ter',
						'fpv_ter',
						'idv_ter',
						'nfv_ter',
						'sqv_ter',
						'tpv_ter',
						'ral_ter',
						'evg_ter',
						'dtg_ter',
						'azt2_ter',
						'abc2_ter',
						'efv2_ter',
						'rpv2_ter',
						'dtf2_ter',
						'lpv2_ter',
						'cantidad_medicamento',
						'adherencia',
						'tiempo_arv',
						'fecha_proxentrega_arv'
					).filter(boleta_clinica=persona['id']).order_by('-fecha_actualizacion')[:1].get()
				)
			except Exception, e:
				seguimiento = False
				pass
			
		except Exception, e:
			persona = False
			seguimiento = False

		#VALIDACIONES DONDE SI TIENE BOLETA INGRESADA MAYOR DE 7 DIAS PUES CREA UNA NUEVA, SINO CARGA LA ANTERIOR
		hoy = datetime.today().date()
		try:
			ultima_boleta = BoletasSeguimientos.objects.filter(boleta_clinica__boleta__identidad=identidad).order_by('-fecha_actualizacion')[:1].get()
			from datetime import timedelta
			dias = timedelta(days=5)
			fecha = datetime.date(ultima_boleta.fecha_actualizacion + dias)
			print ultima_boleta.fecha_actualizacion , fecha, hoy
			if fecha < hoy:
				seguimiento = False
		except Exception, e:
			print e
			pass

		data = {
			'persona' : persona,
			'seg': seguimiento,
		}

		return HttpResponse(json.dumps(data, default=date_handler), content_type='application/json')
	#GET
	elif request.method == 'GET':
		formulario = RPNForm()
		formulario2 = BoletaForm()
		formulario3 = BoletaClinicaSeguimientoForm()
		formulario4 = BoletaSeguimientoForm()
		ctx = {
			'formulario' : formulario,
			'formulario2' : formulario2,
			'formulario3' : formulario3,
			'formulario4' : formulario4,
			'exito': exito,
			'responsable': responsable,
			'embarazada': embarazada,
		}
		return render(request, 'boleta_seguimiento.html', ctx)
	if request.method == 'POST':
		ide = request.POST['identidad']
		identidad = ide.replace("-", "")
		#try:
		with transaction.atomic():
			
			formulario4 = BoletaSeguimientoForm(request.POST)
			if  formulario4.is_valid():
				try:
					instance = BoletasClinicas.objects.get(pk=request.POST.get('boleta_clinica'))
				except Exception, e:
					formulario = RPNForm()
					formulario.fields['sexo'].widget.attrs['disabled'] = True

					formulario2 = BoletaForm()
					formulario3 = BoletaClinicaSeguimientoForm()
					formulario4 = BoletaSeguimientoForm()
					ctx = {
							'formulario' : formulario,
							'formulario2' : formulario2,
							'formulario3' : formulario3,
							'formulario4' : formulario4,
							'error': True,
							'responsable': responsable,
							'embarazada': embarazada,
						}
					return render(request, 'boleta_seguimiento.html', ctx)
				
				formulario3 = BoletaClinicaSeguimientoForm(request.POST, instance=instance)
				registro2 = formulario3.save(commit=False)
				registro2.actualmente_tarv = request.POST.get('actualmente_tarv')
				
				if request.POST.get('fecha_inicio_tarv') != '':
					registro2.fecha_inicio_tarv = request.POST.get('fecha_inicio_tarv')
				else:
					registro2.fecha_inicio_tarv = None
				registro2.estatus_actual_tarv = request.POST.get('estatus_actual_tarv')
				registro2.estado_inmunologico = request.POST.get('estado_inmunologico')
				registro2.hepb_resultado = request.POST.get('hepb_resultado')
				registro2.hepc_resultado = request.POST.get('hepc_resultado')
				registro2.rpr_resultado = request.POST.get('rpr_resultado')
				registro2.estado_clinico= request.POST.get('estado_clinico')
				registro2.lic4= request.POST.get('lic4')
				registro2.lic4_ordenado_consulta= request.POST.get('lic4_ordenado_consulta')
				registro2.caviral= request.POST.get('caviral')
				registro2.caviral_ordenado_consulta= request.POST.get('caviral_ordenado_consulta')
				registro2.hepb= request.POST.get('hepb')
				registro2.hepb_ordenado_consulta= request.POST.get('hepb_ordenado_consulta')
				registro2.hepc= request.POST.get('hepc')
				registro2.hepc_ordenado_consulta= request.POST.get('hepc_ordenado_consulta')
				registro2.rpr= request.POST.get('rpr')
				registro2.rpr_ordenado_consulta= request.POST.get('rpr_ordenado_consulta')
				registro2.rxtorax= request.POST.get('rxtorax')
				registro2.rxtorax_ordenado_consulta= request.POST.get('rxtorax_ordenado_consulta')
				registro2.sespu= request.POST.get('sespu')
				registro2.sespu_ordenado_consulta= request.POST.get('sespu_ordenado_consulta')
				registro2.ppd= request.POST.get('ppd')
				registro2.ppd_ordenado_consulta= request.POST.get('ppd_ordenado_consulta')
				registro2.cultivo= request.POST.get('cultivo')
				registro2.cultivo_ordenado_consulta= request.POST.get('cultivo_ordenado_consulta')
				registro2.usg= request.POST.get('usg')
				registro2.usg_ordenado_consulta= request.POST.get('usg_ordenado_consulta')
				registro2.biopsia= request.POST.get('biopsia')
				registro2.biopsia_ordenado_consulta= request.POST.get('biopsia_ordenado_consulta')
				registro2.otro= request.POST.get('otro')
				registro2.otro_ordenado_consulta= request.POST.get('otro_ordenado_consulta')
				registro2.tupu= request.POST.get('tupu')
				registro2.tupu_initrat= request.POST.get('tupu_initrat')
				registro2.tupu_entrat= request.POST.get('tupu_entrat')
				registro2.tupu_entrat_fintrat= request.POST.get('tupu_entrat_fintrat')
				registro2.tupu_intrat= request.POST.get('tupu_intrat')
				registro2.tupu_intrat_reitrat= request.POST.get('tupu_intrat_reitrat')
				registro2.tupu_trat= request.POST.get('tupu_trat')
				registro2.tudi= request.POST.get('tudi')
				registro2.tudi_initrat= request.POST.get('tudi_initrat')
				registro2.tudi_entrat= request.POST.get('tudi_entrat')
				registro2.tudi_entrat_fintrat= request.POST.get('tudi_entrat_fintrat')
				registro2.tudi_intrat= request.POST.get('tudi_intrat')
				registro2.tudi_intrat_reitrat= request.POST.get('tudi_intrat_reitrat')
				registro2.tudi_trat= request.POST.get('tudi_trat')
				registro2.hepb= request.POST.get('hepb')
				registro2.hepb_initrat= request.POST.get('hepb_initrat')
				registro2.hepb_entrat= request.POST.get('hepb_entrat')
				registro2.hepb_entrat_fintrat= request.POST.get('hepb_entrat_fintrat')
				registro2.hepb_intrat= request.POST.get('hepb_intrat')
				registro2.hepb_intrat_reitrat= request.POST.get('hepb_intrat_reitrat')
				registro2.hepb_trat= request.POST.get('hepb_trat')
				registro2.hepc= request.POST.get('hepc')
				registro2.hepc_initrat= request.POST.get('hepc_initrat')
				registro2.hepc_entrat= request.POST.get('hepc_entrat')
				registro2.hepc_entrat_fintrat= request.POST.get('hepc_entrat_fintrat')
				registro2.hepc_intrat= request.POST.get('hepc_intrat')
				registro2.hepc_intrat_reitrat= request.POST.get('hepc_intrat_reitrat')
				registro2.hepc_trat= request.POST.get('hepc_trat')
				registro2.ulg= request.POST.get('ulg')
				registro2.ulg_initrat= request.POST.get('ulg_initrat')
				registro2.ulg_entrat= request.POST.get('ulg_entrat')
				registro2.ulg_entrat_fintrat= request.POST.get('ulg_entrat_fintrat')
				registro2.ulg_intrat= request.POST.get('ulg_intrat')
				registro2.ulg_intrat_reitrat= request.POST.get('ulg_intrat_reitrat')
				registro2.ulg_trat= request.POST.get('ulg_trat')
				registro2.secure= request.POST.get('secure')
				registro2.secure_initrat= request.POST.get('secure_initrat')
				registro2.secure_entrat= request.POST.get('secure_entrat')
				registro2.secure_entrat_fintrat= request.POST.get('secure_entrat_fintrat')
				registro2.secure_intrat= request.POST.get('secure_intrat')
				registro2.secure_intrat_reitrat= request.POST.get('secure_intrat_reitrat')
				registro2.secure_trat= request.POST.get('secure_trat')
				registro2.fluva= request.POST.get('fluva')
				registro2.fluva_initrat= request.POST.get('fluva_initrat')
				registro2.fluva_entrat= request.POST.get('fluva_entrat')
				registro2.fluva_entrat_fintrat= request.POST.get('fluva_entrat_fintrat')
				registro2.fluva_intrat= request.POST.get('fluva_intrat')
				registro2.fluva_intrat_reitrat= request.POST.get('fluva_intrat_reitrat')
				registro2.fluva_trat= request.POST.get('fluva_trat')
				registro2.buin= request.POST.get('buin')
				registro2.buin_initrat= request.POST.get('buin_initrat')
				registro2.buin_entrat= request.POST.get('buin_entrat')
				registro2.buin_entrat_fintrat= request.POST.get('buin_entrat_fintrat')
				registro2.buin_intrat= request.POST.get('buin_intrat')
				registro2.buin_intrat_reitrat= request.POST.get('buin_intrat_reitrat')
				registro2.buin_trat= request.POST.get('buin_trat')
				registro2.edes= request.POST.get('edes')
				registro2.edes_initrat= request.POST.get('edes_initrat')
				registro2.edes_entrat= request.POST.get('edes_entrat')
				registro2.edes_entrat_fintrat= request.POST.get('edes_entrat_fintrat')
				registro2.edes_intrat= request.POST.get('edes_intrat')
				registro2.edes_intrat_reitrat= request.POST.get('edes_intrat_reitrat')
				registro2.edes_trat= request.POST.get('edes_trat')
				registro2.verge= request.POST.get('verge')
				registro2.verge_initrat= request.POST.get('verge_initrat')
				registro2.verge_entrat= request.POST.get('verge_entrat')
				registro2.verge_entrat_fintrat= request.POST.get('verge_entrat_fintrat')
				registro2.verge_intrat= request.POST.get('verge_intrat')
				registro2.verge_intrat_reitrat= request.POST.get('verge_intrat_reitrat')
				registro2.verge_trat= request.POST.get('verge_trat')
				registro2.trasex= request.POST.get('trasex')
				registro2.trasex_initrat= request.POST.get('trasex_initrat')
				registro2.trasex_entrat= request.POST.get('trasex_entrat')
				registro2.trasex_entrat_fintrat= request.POST.get('trasex_entrat_fintrat')
				registro2.trasex_intrat= request.POST.get('trasex_intrat')
				registro2.trasex_intrat_reitrat= request.POST.get('trasex_intrat_reitrat')
				registro2.trasex_trat= request.POST.get('trasex_trat')
				registro2.proc= request.POST.get('proc')
				registro2.proc_initrat= request.POST.get('proc_initrat')
				registro2.proc_entrat= request.POST.get('proc_entrat')
				registro2.proc_entrat_fintrat= request.POST.get('proc_entrat_fintrat')
				registro2.proc_intrat= request.POST.get('proc_intrat')
				registro2.proc_intrat_reitrat= request.POST.get('proc_intrat_reitrat')
				registro2.proc_trat= request.POST.get('proc_trat')
				registro2.infpel= request.POST.get('infpel')
				registro2.infpel_initrat= request.POST.get('infpel_initrat')
				registro2.infpel_entrat= request.POST.get('infpel_entrat')
				registro2.infpel_entrat_fintrat= request.POST.get('infpel_entrat_fintrat')
				registro2.infpel_intrat= request.POST.get('infpel_intrat')
				registro2.infpel_intrat_reitrat= request.POST.get('infpel_intrat_reitrat')
				registro2.infpel_trat= request.POST.get('infpel_trat')
				registro2.actualizado_por = request.user
				registro2.creado_por = request.user
				if request.POST.get('fecha_ultima_menstruacion') != '':
					registro2.fecha_ultima_menstruacion = request.POST.get('fecha_ultima_menstruacion')
				else:
					registro2.fecha_ultima_menstruacion = None
				if request.POST.get('fecha_cesaria') != '':
					registro2.fecha_cesaria = request.POST.get('fecha_cesaria')
				else:
					registro2.fecha_cesaria = None
				if request.POST.get('fecha_inicio_tarv') != '':
					registro2.fecha_inicio_tarv = request.POST.get('fecha_inicio_tarv')
				else:
					registro2.fecha_inicio_tarv = None
				if request.POST.get('fecha_diagnostico') != '':
					registro2.fecha_diagnostico = request.POST.get('fecha_diagnostico')
				else:
					registro2.fecha_diagnostico = None
				if request.POST.get('fecha_primera_consulta') != '':
					registro2.fecha_primera_consulta = request.POST.get('fecha_primera_consulta')
				else:
					registro2.fecha_primera_consulta = None
				if request.POST.get('fecha_proxima_cita') != '':
					registro2.fecha_proxima_cita = request.POST.get('fecha_proxima_cita')
				else:
					registro2.fecha_proxima_cita = None
				if request.POST.get('lic4_fecha_realizacion') != '':
					registro2.lic4_fecha_realizacion = request.POST.get('lic4_fecha_realizacion')
				else:
					registro2.lic4_fecha_realizacion = None
				if request.POST.get('caviral_fecha_realizacion') != '':
					registro2.caviral_fecha_realizacion = request.POST.get('caviral_fecha_realizacion')
				else:
					registro2.caviral_fecha_realizacion = None
				if request.POST.get('hepb_fecha_realizacion') != '':
					registro2.hepb_fecha_realizacion = request.POST.get('hepb_fecha_realizacion')
				else:
					registro2.hepb_fecha_realizacion = None
				if request.POST.get('hepc_fecha_realizacion') != '':
					registro2.hepc_fecha_realizacion = request.POST.get('hepc_fecha_realizacion')
				else:
					registro2.hepc_fecha_realizacion = None
				if request.POST.get('rpr_fecha_realizacion') != '':
					registro2.rpr_fecha_realizacion = request.POST.get('rpr_fecha_realizacion')
				else:
					registro2.rpr_fecha_realizacion = None
				if request.POST.get('rxtorax_fecha_realizacion') != '':
					registro2.rxtorax_fecha_realizacion = request.POST.get('rxtorax_fecha_realizacion')
				else:
					registro2.rxtorax_fecha_realizacion = None
				if request.POST.get('sespu_fecha_realizacion') != '':
					registro2.sespu_fecha_realizacion = request.POST.get('sespu_fecha_realizacion')
				else:
					registro2.sespu_fecha_realizacion = None
				if request.POST.get('ppd_fecha_realizacion') != '':
					registro2.ppd_fecha_realizacion = request.POST.get('ppd_fecha_realizacion')
				else:
					registro2.ppd_fecha_realizacion = None
				if request.POST.get('cultivo_fecha_realizacion') != '':
					registro2.cultivo_fecha_realizacion = request.POST.get('cultivo_fecha_realizacion')
				else:
					registro2.cultivo_fecha_realizacion = None
				if request.POST.get('usg_fecha_realizacion') != '':
					registro2.usg_fecha_realizacion = request.POST.get('usg_fecha_realizacion')
				else:
					registro2.usg_fecha_realizacion = None
				if request.POST.get('biopsia_fecha_realizacion') != '':
					registro2.biopsia_fecha_realizacion = request.POST.get('biopsia_fecha_realizacion')
				else:
					registro2.biopsia_fecha_realizacion = None
				if request.POST.get('otro_fecha_realizacion') != '':
					registro2.otro_fecha_realizacion = request.POST.get('otro_fecha_realizacion')
				else:
					registro2.otro_fecha_realizacion = None
				if request.POST.get('tupu_diag') != '':
					registro2.tupu_diag = request.POST.get('tupu_diag')
				else:
					registro2.tupu_diag = None
				if request.POST.get('tupu_fecha_initrat') != '':
					registro2.tupu_fecha_initrat = request.POST.get('tupu_fecha_initrat')
				else:
					registro2.tupu_fecha_initrat = None
				if request.POST.get('tupu_entrat_diag') != '':
					registro2.tupu_entrat_diag = request.POST.get('tupu_entrat_diag')
				else:
					registro2.tupu_entrat_diag = None
				if request.POST.get('tupu_entrat_fecha_fintrat') != '':
					registro2.tupu_entrat_fecha_fintrat = request.POST.get('tupu_entrat_fecha_fintrat')
				else:
					registro2.tupu_entrat_fecha_fintrat = None
				if request.POST.get('tupu_intrat_diag') != '':
					registro2.tupu_intrat_diag = request.POST.get('tupu_intrat_diag')
				else:
					registro2.tupu_intrat_diag = None
				if request.POST.get('tupu_intrat_fecha_reitrat') != '':
					registro2.tupu_intrat_fecha_reitrat = request.POST.get('tupu_intrat_fecha_reitrat')
				else:
					registro2.tupu_intrat_fecha_reitrat = None
				if request.POST.get('tudi_diag') != '':
					registro2.tudi_diag = request.POST.get('tudi_diag')
				else:
					registro2.tudi_diag = None
				if request.POST.get('tudi_fecha_initrat') != '':
					registro2.tudi_fecha_initrat = request.POST.get('tudi_fecha_initrat')
				else:
					registro2.tudi_fecha_initrat = None
				if request.POST.get('tudi_entrat_diag') != '':
					registro2.tudi_entrat_diag = request.POST.get('tudi_entrat_diag')
				else:
					registro2.tudi_entrat_diag = None
				if request.POST.get('tudi_entrat_fecha_fintrat') != '':
					registro2.tudi_entrat_fecha_fintrat = request.POST.get('tudi_entrat_fecha_fintrat')
				else:
					registro2.tudi_entrat_fecha_fintrat = None
				if request.POST.get('tudi_intrat_diag') != '':
					registro2.tudi_intrat_diag = request.POST.get('tudi_intrat_diag')
				else:
					registro2.tudi_intrat_diag = None
				if request.POST.get('tudi_intrat_fecha_reitrat') != '':
					registro2.tudi_intrat_fecha_reitrat = request.POST.get('tudi_intrat_fecha_reitrat')
				else:
					registro2.tudi_intrat_fecha_reitrat = None
				if request.POST.get('hepb_diag') != '':
					registro2.hepb_diag = request.POST.get('hepb_diag')
				else:
					registro2.hepb_diag = None
				if request.POST.get('hepb_fecha_initrat') != '':
					registro2.hepb_fecha_initrat = request.POST.get('hepb_fecha_initrat')
				else:
					registro2.hepb_fecha_initrat = None
				if request.POST.get('hepb_entrat_diag') != '':
					registro2.hepb_entrat_diag = request.POST.get('hepb_entrat_diag')
				else:
					registro2.hepb_entrat_diag = None
				if request.POST.get('hepb_entrat_fecha_fintrat') != '':
					registro2.hepb_entrat_fecha_fintrat = request.POST.get('hepb_entrat_fecha_fintrat')
				else:
					registro2.hepb_entrat_fecha_fintrat = None
				if request.POST.get('hepb_intrat_diag') != '':
					registro2.hepb_intrat_diag = request.POST.get('hepb_intrat_diag')
				else:
					registro2.hepb_intrat_diag = None
				if request.POST.get('hepb_intrat_fecha_reitrat') != '':
					registro2.hepb_intrat_fecha_reitrat = request.POST.get('hepb_intrat_fecha_reitrat')
				else:
					registro2.hepb_intrat_fecha_reitrat = None
				if request.POST.get('hepc_diag') != '':
					registro2.hepc_diag = request.POST.get('hepc_diag')
				else:
					registro2.hepc_diag = None
				if request.POST.get('hepc_fecha_initrat') != '':
					registro2.hepc_fecha_initrat = request.POST.get('hepc_fecha_initrat')
				else:
					registro2.hepc_fecha_initrat = None
				if request.POST.get('hepc_entrat_diag') != '':
					registro2.hepc_entrat_diag = request.POST.get('hepc_entrat_diag')
				else:
					registro2.hepc_entrat_diag = None
				if request.POST.get('hepc_entrat_fecha_fintrat') != '':
					registro2.hepc_entrat_fecha_fintrat = request.POST.get('hepc_entrat_fecha_fintrat')
				else:
					registro2.hepc_entrat_fecha_fintrat = None
				if request.POST.get('hepc_intrat_diag') != '':
					registro2.hepc_intrat_diag = request.POST.get('hepc_intrat_diag')
				else:
					registro2.hepc_intrat_diag = None
				if request.POST.get('hepc_intrat_fecha_reitrat') != '':
					registro2.hepc_intrat_fecha_reitrat = request.POST.get('hepc_intrat_fecha_reitrat')
				else:
					registro2.hepc_intrat_fecha_reitrat = None
				if request.POST.get('ulg_diag') != '':
					registro2.ulg_diag = request.POST.get('ulg_diag')
				else:
					registro2.ulg_diag = None
				if request.POST.get('ulg_fecha_initrat') != '':
					registro2.ulg_fecha_initrat = request.POST.get('ulg_fecha_initrat')
				else:
					registro2.ulg_fecha_initrat = None
				if request.POST.get('ulg_entrat_diag') != '':
					registro2.ulg_entrat_diag = request.POST.get('ulg_entrat_diag')
				else:
					registro2.ulg_entrat_diag = None
				if request.POST.get('ulg_entrat_fecha_fintrat') != '':
					registro2.ulg_entrat_fecha_fintrat = request.POST.get('ulg_entrat_fecha_fintrat')
				else:
					registro2.ulg_entrat_fecha_fintrat = None
				if request.POST.get('ulg_intrat_diag') != '':
					registro2.ulg_intrat_diag = request.POST.get('ulg_intrat_diag')
				else:
					registro2.ulg_intrat_diag = None
				if request.POST.get('ulg_intrat_fecha_reitrat') != '':
					registro2.ulg_intrat_fecha_reitrat = request.POST.get('ulg_intrat_fecha_reitrat')
				else:
					registro2.ulg_intrat_fecha_reitrat = None
				if request.POST.get('secure_diag') != '':
					registro2.secure_diag = request.POST.get('secure_diag')
				else:
					registro2.secure_diag = None
				if request.POST.get('secure_fecha_initrat') != '':
					registro2.secure_fecha_initrat = request.POST.get('secure_fecha_initrat')
				else:
					registro2.secure_fecha_initrat = None
				if request.POST.get('secure_entrat_diag') != '':
					registro2.secure_entrat_diag = request.POST.get('secure_entrat_diag')
				else:
					registro2.secure_entrat_diag = None
				if request.POST.get('secure_entrat_fecha_fintrat') != '':
					registro2.secure_entrat_fecha_fintrat = request.POST.get('secure_entrat_fecha_fintrat')
				else:
					registro2.secure_entrat_fecha_fintrat = None
				if request.POST.get('secure_intrat_diag') != '':
					registro2.secure_intrat_diag = request.POST.get('secure_intrat_diag')
				else:
					registro2.secure_intrat_diag = None
				if request.POST.get('secure_intrat_fecha_reitrat') != '':
					registro2.secure_intrat_fecha_reitrat = request.POST.get('secure_intrat_fecha_reitrat')
				else:
					registro2.secure_intrat_fecha_reitrat = None
				if request.POST.get('fluva_diag') != '':
					registro2.fluva_diag = request.POST.get('fluva_diag')
				else:
					registro2.fluva_diag = None
				if request.POST.get('fluva_fecha_initrat') != '':
					registro2.fluva_fecha_initrat = request.POST.get('fluva_fecha_initrat')
				else:
					registro2.fluva_fecha_initrat = None
				if request.POST.get('fluva_entrat_diag') != '':
					registro2.fluva_entrat_diag = request.POST.get('fluva_entrat_diag')
				else:
					registro2.fluva_entrat_diag = None
				if request.POST.get('fluva_entrat_fecha_fintrat') != '':
					registro2.fluva_entrat_fecha_fintrat = request.POST.get('fluva_entrat_fecha_fintrat')
				else:
					registro2.fluva_entrat_fecha_fintrat = None
				if request.POST.get('fluva_intrat_diag') != '':
					registro2.fluva_intrat_diag = request.POST.get('fluva_intrat_diag')
				else:
					registro2.fluva_intrat_diag = None
				if request.POST.get('fluva_intrat_fecha_reitrat') != '':
					registro2.fluva_intrat_fecha_reitrat = request.POST.get('fluva_intrat_fecha_reitrat')
				else:
					registro2.fluva_intrat_fecha_reitrat = None
				if request.POST.get('buin_diag') != '':
					registro2.buin_diag = request.POST.get('buin_diag')
				else:
					registro2.buin_diag = None
				if request.POST.get('buin_fecha_initrat') != '':
					registro2.buin_fecha_initrat = request.POST.get('buin_fecha_initrat')
				else:
					registro2.buin_fecha_initrat = None
				if request.POST.get('buin_entrat_diag') != '':
					registro2.buin_entrat_diag = request.POST.get('buin_entrat_diag')
				else:
					registro2.buin_entrat_diag = None
				if request.POST.get('buin_entrat_fecha_fintrat') != '':
					registro2.buin_entrat_fecha_fintrat = request.POST.get('buin_entrat_fecha_fintrat')
				else:
					registro2.buin_entrat_fecha_fintrat = None
				if request.POST.get('buin_intrat_diag') != '':
					registro2.buin_intrat_diag = request.POST.get('buin_intrat_diag')
				else:
					registro2.buin_intrat_diag = None
				if request.POST.get('buin_intrat_fecha_reitrat') != '':
					registro2.buin_intrat_fecha_reitrat = request.POST.get('buin_intrat_fecha_reitrat')
				else:
					registro2.buin_intrat_fecha_reitrat = None
				if request.POST.get('edes_diag') != '':
					registro2.edes_diag = request.POST.get('edes_diag')
				else:
					registro2.edes_diag = None
				if request.POST.get('edes_fecha_initrat') != '':
					registro2.edes_fecha_initrat = request.POST.get('edes_fecha_initrat')
				else:
					registro2.edes_fecha_initrat = None
				if request.POST.get('edes_entrat_diag') != '':
					registro2.edes_entrat_diag = request.POST.get('edes_entrat_diag')
				else:
					registro2.edes_entrat_diag = None
				if request.POST.get('edes_entrat_fecha_fintrat') != '':
					registro2.edes_entrat_fecha_fintrat = request.POST.get('edes_entrat_fecha_fintrat')
				else:
					registro2.edes_entrat_fecha_fintrat = None
				if request.POST.get('edes_intrat_diag') != '':
					registro2.edes_intrat_diag = request.POST.get('edes_intrat_diag')
				else:
					registro2.edes_intrat_diag = None
				if request.POST.get('edes_intrat_fecha_reitrat') != '':
					registro2.edes_intrat_fecha_reitrat = request.POST.get('edes_intrat_fecha_reitrat')
				else:
					registro2.edes_intrat_fecha_reitrat = None
				if request.POST.get('verge_diag') != '':
					registro2.verge_diag = request.POST.get('verge_diag')
				else:
					registro2.verge_diag = None
				if request.POST.get('verge_fecha_initrat') != '':
					registro2.verge_fecha_initrat = request.POST.get('verge_fecha_initrat')
				else:
					registro2.verge_fecha_initrat = None
				if request.POST.get('verge_entrat_diag') != '':
					registro2.verge_entrat_diag = request.POST.get('verge_entrat_diag')
				else:
					registro2.verge_entrat_diag = None
				if request.POST.get('verge_entrat_fecha_fintrat') != '':
					registro2.verge_entrat_fecha_fintrat = request.POST.get('verge_entrat_fecha_fintrat')
				else:
					registro2.verge_entrat_fecha_fintrat = None
				if request.POST.get('verge_intrat_diag') != '':
					registro2.verge_intrat_diag = request.POST.get('verge_intrat_diag')
				else:
					registro2.verge_intrat_diag = None
				if request.POST.get('verge_intrat_fecha_reitrat') != '':
					registro2.verge_intrat_fecha_reitrat = request.POST.get('verge_intrat_fecha_reitrat')
				else:
					registro2.verge_intrat_fecha_reitrat = None
				if request.POST.get('trasex_diag') != '':
					registro2.trasex_diag = request.POST.get('trasex_diag')
				else:
					registro2.trasex_diag = None
				if request.POST.get('trasex_fecha_initrat') != '':
					registro2.trasex_fecha_initrat = request.POST.get('trasex_fecha_initrat')
				else:
					registro2.trasex_fecha_initrat = None
				if request.POST.get('trasex_entrat_diag') != '':
					registro2.trasex_entrat_diag = request.POST.get('trasex_entrat_diag')
				else:
					registro2.trasex_entrat_diag = None
				if request.POST.get('trasex_entrat_fecha_fintrat') != '':
					registro2.trasex_entrat_fecha_fintrat = request.POST.get('trasex_entrat_fecha_fintrat')
				else:
					registro2.trasex_entrat_fecha_fintrat = None
				if request.POST.get('trasex_intrat_diag') != '':
					registro2.trasex_intrat_diag = request.POST.get('trasex_intrat_diag')
				else:
					registro2.trasex_intrat_diag = None
				if request.POST.get('trasex_intrat_fecha_reitrat') != '':
					registro2.trasex_intrat_fecha_reitrat = request.POST.get('trasex_intrat_fecha_reitrat')
				else:
					registro2.trasex_intrat_fecha_reitrat = None
				if request.POST.get('proc_diag') != '':
					registro2.proc_diag = request.POST.get('proc_diag')
				else:
					registro2.proc_diag = None
				if request.POST.get('proc_fecha_initrat') != '':
					registro2.proc_fecha_initrat = request.POST.get('proc_fecha_initrat')
				else:
					registro2.proc_fecha_initrat = None
				if request.POST.get('proc_entrat_diag') != '':
					registro2.proc_entrat_diag = request.POST.get('proc_entrat_diag')
				else:
					registro2.proc_entrat_diag = None
				if request.POST.get('proc_entrat_fecha_fintrat') != '':
					registro2.proc_entrat_fecha_fintrat = request.POST.get('proc_entrat_fecha_fintrat')
				else:
					registro2.proc_entrat_fecha_fintrat = None
				if request.POST.get('proc_intrat_diag') != '':
					registro2.proc_intrat_diag = request.POST.get('proc_intrat_diag')
				else:
					registro2.proc_intrat_diag = None
				if request.POST.get('proc_intrat_fecha_reitrat') != '':
					registro2.proc_intrat_fecha_reitrat = request.POST.get('proc_intrat_fecha_reitrat')
				else:
					registro2.proc_intrat_fecha_reitrat = None
				if request.POST.get('infpel_diag') != '':
					registro2.infpel_diag = request.POST.get('infpel_diag')
				else:
					registro2.infpel_diag = None
				if request.POST.get('infpel_fecha_initrat') != '':
					registro2.infpel_fecha_initrat = request.POST.get('infpel_fecha_initrat')
				else:
					registro2.infpel_fecha_initrat = None
				if request.POST.get('infpel_entrat_diag') != '':
					registro2.infpel_entrat_diag = request.POST.get('infpel_entrat_diag')
				else:
					registro2.infpel_entrat_diag = None
				if request.POST.get('infpel_entrat_fecha_fintrat') != '':
					registro2.infpel_entrat_fecha_fintrat = request.POST.get('infpel_entrat_fecha_fintrat')
				else:
					registro2.infpel_entrat_fecha_fintrat = None
				if request.POST.get('infpel_intrat_diag') != '':
					registro2.infpel_intrat_diag = request.POST.get('infpel_intrat_diag')
				else:
					registro2.infpel_intrat_diag = None
				if request.POST.get('infpel_intrat_fecha_reitrat') != '':	
					registro2.infpel_intrat_fecha_reitrat = request.POST.get('infpel_intrat_fecha_reitrat')
				else:
					registro2.infpel_intrat_fecha_reitrat = None

				try:
					responsable = Responsables.objects.get(usuario_sistema=request.user)
					registro2.establecimiento = responsable.establecimiento
				except Exception, e:
					registro2.establecimiento = None

				registro2.save()

				try:
					instance = BoletasSeguimientos.objects.get(pk=request.POST.get('boleta_seg'))
					formulario4 = BoletaSeguimientoForm(request.POST, instance=instance)
					registro = formulario4.save(commit=False)
				except Exception, e:
					formulario4 = BoletaSeguimientoForm(request.POST)
					registro = formulario4.save(commit=False)
					registro.creado_por = request.user

				registro.actualizado_por = request.user
				registro.boleta_clinica = registro2
				registro.identidad =  identidad
				if '1' in request.POST.getlist('co1'):
					registro.azt = True
				else:
					registro.azt = False 
				if '2' in request.POST.getlist('co1'):
					registro.abc = True
				else:
					registro.abc = False 
				if '3' in request.POST.getlist('co1'):
					registro.efv = True
				else:
					registro.efv = False 
				if '4' in request.POST.getlist('co1'):
					registro.rpv = True
				else:
					registro.rpv = False 
				if '5' in request.POST.getlist('co1'):
					registro.dtf = True
				else:
					registro.dtf = False 
				if '6' in request.POST.getlist('co1'):
					registro.lpv = True
				else:
					registro.lpv = False 

				if '1' in request.POST.getlist('medicamento_prescritos'):
					registro.abc_med = True
				else:
						registro.abc_med = False
				if '2' in request.POST.getlist('medicamento_prescritos'):
					registro.ft_med = True
				else:
						registro.ft_med = False
				if '3' in request.POST.getlist('medicamento_prescritos'):
					registro.d4t_med = True
				else:
						registro.d4t_med = False
				if '4' in request.POST.getlist('medicamento_prescritos'):
					registro.azt_med = True
				else:
						registro.azt_med = False
				if '5' in request.POST.getlist('medicamento_prescritos'):
					registro.efv_med = True
				else:
						registro.efv_med = False
				if '6' in request.POST.getlist('medicamento_prescritos'):
					registro.nvp_med = True
				else:
						registro.nvp_med = False
				if '7' in request.POST.getlist('medicamento_prescritos'):
					registro.ddi_med = True
				else:
						registro.ddi_med = False
				if '8' in request.POST.getlist('medicamento_prescritos'):
					registro.tc_med = True
				else:
						registro.tc_med = False
				if '9' in request.POST.getlist('medicamento_prescritos'):
					registro.tdf_med = True
				else:
						registro.tdf_med = False
				if '10' in request.POST.getlist('medicamento_prescritos'):
					registro.rpv_med = True
				else:
						registro.rpv_med = False
				if '11' in request.POST.getlist('medicamento_prescritos'):
					registro.etr_med = True
				else:
						registro.etr_med = False
				if '12' in request.POST.getlist('medicamento_prescritos'):
					registro.atv_med = True
				else:
						registro.atv_med = False
				if '13' in request.POST.getlist('medicamento_prescritos'):
					registro.drv_med = True
				else:
						registro.drv_med = False
				if '14' in request.POST.getlist('medicamento_prescritos'):
					registro.fpv_med = True
				else:
						registro.fpv_med = False
				if '15' in request.POST.getlist('medicamento_prescritos'):
					registro.idv_med = True
				else:
						registro.idv_med = False
				if '16' in request.POST.getlist('medicamento_prescritos'):
					registro.nfv_med = True
				else:
						registro.nfv_med = False
				if '17' in request.POST.getlist('medicamento_prescritos'):
					registro.sqv_med = True
				else:
						registro.sqv_med = False
				if '18' in request.POST.getlist('medicamento_prescritos'):
					registro.tpv_med = True
				else:
						registro.tpv_med = False
				if '19' in request.POST.getlist('medicamento_prescritos'):
					registro.ral_med = True
				else:
						registro.ral_med = False
				if '20' in request.POST.getlist('medicamento_prescritos'):
					registro.evg_med = True
				else:
						registro.evg_med = False
				if '21' in request.POST.getlist('medicamento_prescritos'):
					registro.dtg_med = True
				else:
						registro.dtg_med = False

				if '1' in request.POST.getlist('co2'):
					registro.azt2_ter = True
				else:
					registro.azt2_ter = False 
				if '2' in request.POST.getlist('co2'):
					registro.abc2_ter = True
				else:
					registro.abc2_ter = False 
				if '3' in request.POST.getlist('co2'):
					registro.efv2_ter = True
				else:
					registro.efv2_ter = False 
				if '4' in request.POST.getlist('co2'):
					registro.rpv2_ter = True
				else:
					registro.rpv2_ter = False 
				if '5' in request.POST.getlist('co2'):
					registro.dtf2_ter = True
				else:
					registro.dtf2_ter = False 
				if '6' in request.POST.getlist('co2'):
					registro.lpv2_ter = True
				else:
					registro.lpv2_ter = False 

				if '1' in request.POST.getlist('terapia'):
					registro.abc_ter = True
				else:
						registro.abc_ter = False
				if '2' in request.POST.getlist('terapia'):
					registro.ft_ter = True
				else:
						registro.ft_ter = False
				if '3' in request.POST.getlist('terapia'):
					registro.d4t_ter = True
				else:
						registro.d4t_ter = False
				if '4' in request.POST.getlist('terapia'):
					registro.azt_ter = True
				else:
						registro.azt_ter = False
				if '5' in request.POST.getlist('terapia'):
					registro.efv_ter = True
				else:
						registro.efv_ter = False
				if '6' in request.POST.getlist('terapia'):
					registro.nvp_ter = True
				else:
						registro.nvp_ter = False
				if '7' in request.POST.getlist('terapia'):
					registro.ddi_ter = True
				else:
						registro.ddi_ter = False
				if '8' in request.POST.getlist('terapia'):
					registro.tc_ter = True
				else:
						registro.tc_ter = False
				if '9' in request.POST.getlist('terapia'):
					registro.tdf_ter = True
				else:
						registro.tdf_ter = False
				if '10' in request.POST.getlist('terapia'):
					registro.rpv_ter = True
				else:
						registro.rpv_ter = False
				if '11' in request.POST.getlist('terapia'):
					registro.etr_ter = True
				else:
						registro.etr_ter = False
				if '12' in request.POST.getlist('terapia'):
					registro.atv_ter = True
				else:
						registro.atv_ter = False
				if '13' in request.POST.getlist('terapia'):
					registro.drv_ter = True
				else:
						registro.drv_ter = False
				if '14' in request.POST.getlist('terapia'):
					registro.fpv_ter = True
				else:
						registro.fpv_ter = False
				if '15' in request.POST.getlist('terapia'):
					registro.idv_ter = True
				else:
						registro.idv_ter = False
				if '16' in request.POST.getlist('terapia'):
					registro.nfv_ter = True
				else:
						registro.nfv_ter = False
				if '17' in request.POST.getlist('terapia'):
					registro.sqv_ter = True
				else:
						registro.sqv_ter = False
				if '18' in request.POST.getlist('terapia'):
					registro.tpv_ter = True
				else:
						registro.tpv_ter = False
				if '19' in request.POST.getlist('terapia'):
					registro.ral_ter = True
				else:
						registro.ral_ter = False
				if '20' in request.POST.getlist('terapia'):
					registro.evg_ter = True
				else:
						registro.evg_ter = False
				if '21' in request.POST.getlist('terapia'):
					registro.dtg_ter = True
				else:
						registro.dtg_ter = False

				registro.conteo_cd4 = request.POST.get('conteo_cd4')
				registro.causa_fallecido = request.POST.get('causa_fallecido')
				registro.motivo = request.POST.get('motivo')
				registro.profpri = request.POST.get('profpri')
				registro.tmpsmx = request.POST.get('tmpsmx')
				registro.tmpsmx_initrat = request.POST.get('tmpsmx_initrat')
				registro.tmpsmx_fintrat = request.POST.get('tmpsmx_fintrat')
				registro.tmpsmx_intrat = request.POST.get('tmpsmx_intrat')
				registro.tmpsmx_reitrat = request.POST.get('tmpsmx_reitrat')
				registro.isoniacida = request.POST.get('isoniacida')
				registro.isoniacida_initrat = request.POST.get('isoniacida_initrat')
				registro.isoniacida_fintrat = request.POST.get('isoniacida_fintrat')
				registro.isoniacida_intrat = request.POST.get('isoniacida_intrat')
				registro.isoniacida_reitrat = request.POST.get('isoniacida_reitrat')
				registro.azitromicida = request.POST.get('azitromicida')
				registro.azitromicida_initrat = request.POST.get('azitromicida_initrat')
				registro.azitromicida_fintrat = request.POST.get('azitromicida_fintrat')
				registro.azitromicida_intrat = request.POST.get('azitromicida_intrat')
				registro.azitromicida_reitrat = request.POST.get('azitromicida_reitrat')
				registro.esquema_arv = request.POST.get('esquema_arv')
				registro.cambio_terapia = request.POST.get('cambio_terapia')
				registro.motivo_cambio_terapia = request.POST.get('motivo_cambio_terapia')
				registro.documentado_con = request.POST.get('documentado_con')
				registro.esquema_actual_arv = request.POST.get('esquema_actual_arv')
				registro.abandono = request.POST.get('abandono')
				registro.suspension = request.POST.get('suspension')
				registro.activo = request.POST.get('activo')
				registro.fallecido = request.POST.get('fallecido')
				registro.fallecido = request.POST.get('fallecido')
				if request.POST.get('fecha_consulta') != '':
					registro.fecha_consulta = request.POST.get('fecha_consulta')
				else:
					registro.fecha_consulta = None
				if request.POST.get('fecha_proxima_cita') != '':
					registro.fecha_proxima_cita = request.POST.get('fecha_proxima_cita')
				else:
					registro.fecha_proxima_cita = None
				if request.POST.get('tmpsmx_fecha_initrat') != '':
					registro.tmpsmx_fecha_initrat = request.POST.get('tmpsmx_fecha_initrat')
				else:
					registro.tmpsmx_fecha_initrat = None
				if request.POST.get('tmpsmx_fecha_fintrat') != '':
					registro.tmpsmx_fecha_fintrat = request.POST.get('tmpsmx_fecha_fintrat')
				else:
					registro.tmpsmx_fecha_fintrat = None
				if request.POST.get('tmpsmx_fecha_intrat') != '':
					registro.tmpsmx_fecha_intrat = request.POST.get('tmpsmx_fecha_intrat')
				else:
					registro.tmpsmx_fecha_intrat = None
				if request.POST.get('tmpsmx_fecha_reitrat') != '':
					registro.tmpsmx_fecha_reitrat = request.POST.get('tmpsmx_fecha_reitrat')
				else:
					registro.tmpsmx_fecha_reitrat = None
				if request.POST.get('isoniacida_fecha_initrat') != '':
					registro.isoniacida_fecha_initrat = request.POST.get('isoniacida_fecha_initrat')
				else:
					registro.isoniacida_fecha_initrat = None
				if request.POST.get('isoniacida_fecha_fintrat') != '':
					registro.isoniacida_fecha_fintrat = request.POST.get('isoniacida_fecha_fintrat')
				else:
					registro.isoniacida_fecha_fintrat = None
				if request.POST.get('isoniacida_fecha_intrat') != '':
					registro.isoniacida_fecha_intrat = request.POST.get('isoniacida_fecha_intrat')
				else:
					registro.isoniacida_fecha_intrat = None
				if request.POST.get('isoniacida_fecha_reitrat') != '':
					registro.isoniacida_fecha_reitrat = request.POST.get('isoniacida_fecha_reitrat')
				else:
					registro.isoniacida_fecha_reitrat = None
				if request.POST.get('azitromicida_fecha_initrat') != '':
					registro.azitromicida_fecha_initrat = request.POST.get('azitromicida_fecha_initrat')
				else:
					registro.azitromicida_fecha_initrat = None
				if request.POST.get('azitromicida_fecha_fintrat') != '':
					registro.azitromicida_fecha_fintrat = request.POST.get('azitromicida_fecha_fintrat')
				else:
					registro.azitromicida_fecha_fintrat = None
				if request.POST.get('azitromicida_fecha_intrat') != '':
					registro.azitromicida_fecha_intrat = request.POST.get('azitromicida_fecha_intrat')
				else:
					registro.azitromicida_fecha_intrat = None
				if request.POST.get('azitromicida_fecha_reitrat') != '':
					registro.azitromicida_fecha_reitrat = request.POST.get('azitromicida_fecha_reitrat')
				else:
					registro.azitromicida_fecha_reitrat = None
				if request.POST.get('arv_fecha_ini') != '':
					registro.arv_fecha_ini = request.POST.get('arv_fecha_ini')
				else:
					registro.arv_fecha_ini = None
				if request.POST.get('fecha_abandono') != '':
					registro.fecha_abandono = request.POST.get('fecha_abandono')
				else:
					registro.fecha_abandono = None
				if request.POST.get('fecha_suspension') != '':
					registro.fecha_suspension = request.POST.get('fecha_suspension')
				else:
					registro.fecha_suspension = None
				if request.POST.get('fecha_reinicio') != '':
					registro.fecha_reinicio = request.POST.get('fecha_reinicio')
				else:
					registro.fecha_reinicio = None
				if request.POST.get('fecha_fallecido') != '':
					registro.fecha_fallecido = request.POST.get('fecha_fallecido')
				else:
					registro.fecha_fallecido = None
				if request.POST.get('fecha_prescripcion_arv') != '':
					registro.fecha_prescripcion_arv = request.POST.get('fecha_prescripcion_arv')
				else:
					registro.fecha_prescripcion_arv = None
				if request.POST.get('fecha_cambio_terapia') != '':
					registro.fecha_cambio_terapia = request.POST.get('fecha_cambio_terapia')
				else:
					registro.fecha_cambio_terapia = None
				if request.POST.get('fecha_entrega_arv') != '':
					registro.fecha_entrega_arv = request.POST.get('fecha_entrega_arv')
				else:
					registro.fecha_entrega_arv = None
				if request.POST.get('fecha_proxentrega_arv') != '':
					registro.fecha_proxentrega_arv = request.POST.get('fecha_proxentrega_arv')
				else:
					registro.fecha_proxentrega_arv = None	 			
	 			registro.save()

				formulario = RPNForm()
				formulario.fields['sexo'].widget.attrs['disabled'] = True

				formulario2 = BoletaForm()
				formulario3 = BoletaClinicaSeguimientoForm()
				formulario4 = BoletaSeguimientoForm()
				exito = True

			else:
				pass
		#except Exception, e:
		#	raise e
		#	print 'ERROR', e
		
		ctx = {
			'formulario' : formulario,
			'formulario2' : formulario2,
			'formulario3' : formulario3,
			'formulario4' : formulario4,
			'exito': exito,
			'responsable': responsable,
			'embarazada': embarazada,
		}
		return render(request, 'boleta_seguimiento.html', ctx)

from datetime import datetime
@login_required()
def reporte_general(request):
	query ={}
	try:
		responsable = usuario(request.user.pk)
		query['establecimiento'] = responsable.establecimiento

		if request.method == 'POST':
			from datetime import timedelta
			fecha = request.POST.get('fecha')
			n_days_ago = (datetime.strptime(fecha, "%Y-%m-%d") + timedelta(days=1))

			query['fecha_creacion__range']= [fecha ,n_days_ago]

		listado = Boletas.objects.values(
			'identidad',
			'expediente',
			'fecha_creacion',
			'creado_por__username'
		).filter(**query).order_by('-fecha_actualizacion').annotate(
			consejeria=Count('boletasconsejeria__id'), 
			postprueba=Count('boletasconsejeriapostprueba__id'),  
			prueba=Count('boletaspruebas__id'), 
			clinica=Count('boletasclinicas__id'),
			seguimiento=Count('boletasclinicas__boletasseguimientos__id')
		)

		print listado.query

	except Exception, e:
		responsable = ''
		listado = False

	ctx = {
		'responsable' : responsable,
		'listado': listado,
	}
	return render(request, 'reporte_general.html', ctx)

@login_required()
def reporte_intervenciones(request):
	query ={}
	try:
		responsable = usuario(request.user.pk)
		query['establecimiento'] = responsable.establecimiento

		if request.method == 'POST':
			from datetime import timedelta
			fecha = request.POST.get('fecha')
			n_days_ago = (datetime.strptime(fecha, "%Y-%m-%d") + timedelta(days=1))
			query['fecha_creacion__range']= [fecha ,n_days_ago]
			
		asistencia = Asistencia.objects.values_list('pk', flat=True).filter(**query).order_by('-fecha_actualizacion')
		listados = Asistencia.objects.extra({'fecha_cast': "CAST(fecha_creacion as DATE)"}).values('lugar',
			'poblacion',
			'intervencion',
			'responsable',
			'coordinador',
			'identidad_reclutador',
			'id',
			'creado_por__first_name',
			'creado_por__last_name',
			'fecha_cast'
		).filter(**query).order_by('-fecha_actualizacion')

		listado_asistencia = ListadoAsistencia.objects.values(
			'asistencia__id',
			'identidad',
			'nombres',
			'correo_electronico',
			'edad',
			'telefono',
			'cantidad_condones',
		).filter(asistencia__in=asistencia)

		
		intervenciones = []
		for listado in listados:
			data = []
			data_asis = []
			for asistencia in listado_asistencia:
				if asistencia['asistencia__id'] == listado['id']:
					data_asis.append(asistencia['identidad'])

			if listado['poblacion'] == 1:
				listado['poblacion'] = "MTS"
			else:
				listado['poblacion'] =  "HSH/TG"

			if listado['intervencion'] == 1:
				listado['intervencion'] = "Proveer o referir a Servicios de Consejeria y Prueba"			
			elif listado['intervencion'] == 2:
				listado['intervencion'] = "Promocion y Distribucion de Condones y Lubricantes"
			elif listado['intervencion'] == 2:
				listado['intervencion'] = "Referencia a Tamizaje, Prevencion y Tratamiento de ITS"
			elif listado['intervencion'] == 2:
				listado['intervencion'] = "Difusion/Alcance y Empoderamiento"
			elif listado['intervencion'] == 2:
				listado['intervencion'] = "Abordaje para IEC"
			else:
				listado['intervencion']="Referencia Salud Reproductiva (Planificacion Familiar)"

			data.append({
				'poblacion': listado['poblacion'],
				'intervencion': listado['intervencion'],
				'responsable': listado['responsable'],
				'coordinador': listado['coordinador'],
				'identidad_reclutador': listado['identidad_reclutador'],
				'id': listado['id'],
				'usuario': listado['creado_por__first_name'] + ' ' + listado['creado_por__last_name'],
				'asistencia':data_asis,
				'fecha': listado['fecha_cast']
			})

			intervenciones.append(data)
	except Exception as e:
		responsable = False
		intervenciones = {}
	ctx = {
		'responsable' : responsable,
		'listado': intervenciones,
	}
	return render(request, 'reporte_intervenciones.html', ctx)