from __future__ import unicode_literals

from django.shortcuts import render
from django.http import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.urls import reverse

from general.forms import *

@login_required()
def principal(request):
	return render(request, 'principal.html')


@login_required()
def pre_prueba_vih(request):
	exito = False
	formulario = RPNForm()
	ctx = {
		'formulario' : formulario,
		#'formulario2': formulario2,
		'exito': exito,
	}
	return render(request, 'pre_prueba_vih.html', ctx)
