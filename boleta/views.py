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
	return Responsables.objects.get(usuario_sistema__id=id)

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
					'barrio',
					'condiciones',
					'otro_condicion',
				).get(identidad=identidad)
			)
		except Exception, e:
			print e, 'ERROR'
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
		ide = request.POST['identidad']
		identidad = ide.replace("-", "")
		#try:
		with transaction.atomic():
			tipo_persona = request.POST['persona']
			print tipo_persona, request.POST.get('sexo_persona'), 'PASO POR AQUI'

			print '---------------------------------------------------------' 
			#print request.POST
			
			formulario = RPNForm(request.POST)
			formulario2 = BoletaForm(request.POST)
			formulario3 = BoletaClinicaForm(request.POST)
			if  formulario2.is_valid() and formulario3.is_valid():
				if str(tipo_persona) != '2':
					print 'SIN BOLETA'
					registro = formulario2.save(commit=False)
					registro.expediente =  identidad +'-'+ request.POST['fecha_nacimiento'] +'-'+ request.POST['sexo_persona']
					registro.ciudad =  Ciudades.objects.get(pk=request.POST['ciudad'])
					registro.municipio =  Municipios.objects.get(pk=request.POST['municipio'])
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
				else:
					#CON BOLETA
					instance = Boletas.objects.get(identidad=identidad)
					formulario2 = BoletaForm(request.POST, instance=instance)
					registro = formulario2.save(commit=False)
					registro.sexo = request.POST['sexo_persona']
					registro.expediente =  identidad +'-'+ request.POST['fecha_nacimiento'] +'-'+ request.POST['sexo_persona']
					registro.municipio =  Municipios.objects.get(pk=request.POST['municipio'])
					registro.ciudad =  Ciudades.objects.get(pk=request.POST['ciudad'])
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

				registro2 = formulario3.save(commit=False)
				registro2.boleta = registro
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
				registro2.creado_por = request.user
				try:
					responsable = Responsables.objects.get(usuario_sistema=request.user)
					registro2.establecimiento = responsable.establecimiento
				except Exception, e:
					registro2.establecimiento = responsable.establecimiento

				print request.POST
				registro2.save()

				formulario = RPNForm()
				formulario.fields['sexo'].widget.attrs['disabled'] = True

				formulario2 = BoletaForm()
				formulario3 = BoletaClinicaForm()
				exito = True

			else:
				print 'AAAAAAAAAAAAAAAAAAAAAAAAA'
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