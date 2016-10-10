
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.http import *
from django.template import RequestContext
from django.urls import reverse
from django.contrib.auth import authenticate, login as auth_login, logout

from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers  import make_password
from django.db import transaction, IntegrityError
from general.forms import *

def cerrar_sesion(request):
	logout(request)
	return redirect('login')

def login(request):
	ctx = {}
	logout(request)
	if request.POST:
		username = request.POST['username']
		password = request.POST['password']

		user = authenticate(username=username, password=password)
		if user is not None:
			if user.is_active:
				auth_login(request, user)
				return HttpResponseRedirect(reverse('principal'))
		else:
			ctx = {
				'error': True,
				'username': username,
			}
	return render(request, 'login.html', ctx)

def registrate(request):
	ctx = {}
	logout(request)
	if request.POST:
		
		from django.core.mail import EmailMultiAlternatives
		subject = 'Peticion De Registro'
		text_content = 'Mensaje...nLinea 2nLinea3'
		html_content = 'Tienes una nueva Peticion de Registro: <br> <br> Nombre:<b>'+ request.POST.get('nombre') +'</b> <br> Telefono:<b>'+ request.POST.get('telefono') +'</b> <br> Correo: <b>'+ request.POST.get('correo') +'</b><br> Comentario: <b>'+ request.POST.get('observaciones') +'</b> <br>'
		from_email = 'kshernandez90@gmail.com' 
		to = 'kshernandez90@gmail.com'
		msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
		msg.attach_alternative(html_content, "text/html")
		msg.send()
		ctx = { 'exito': True }
	else:
		pass
	return render(request, 'registrate.html', ctx)

@login_required()
@transaction.atomic
def crear_usuario(request):
	exito = False
	if request.method== 'POST':
		formulario = UsuarioForm(request.POST)
		formulario2 = UsuarioResponsableForm(request.POST)
		print 'aksjdhaksjdhakshdakhj'
		if formulario.is_valid() and formulario2.is_valid():
			try:
				with transaction.atomic():
					usuario = formulario.save(commit=False)
					usuario.password = make_password(request.POST['password'])
					usuario.first_name = request.POST['nombres']
					usuario.last_name = request.POST['primer_apellido']
					usuario.save()
					formulario.save_m2m()

					responsable = formulario2.save(commit=False)
					responsable.usuario_sistema = usuario
					responsable.save()
					
					formulario = UsuarioForm()
					formulario2 = UsuarioResponsableForm()
					exito = True
			except IntegrityError, e:
				print e
	else:
		formulario = UsuarioForm()
		formulario2 = UsuarioResponsableForm()
	ctx = {
		'formulario' : formulario,
		'formulario2': formulario2,
		'exito': exito,
	}
	return render(request, 'crear_usuario.html', ctx)


@login_required()
def principal(request):
	return render(request, 'principal.html')