
from __future__ import unicode_literals

from django.shortcuts import render
from django.http import *
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login as auth_login, logout
from django.urls import reverse

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

@login_required()
def principal(request):
	return render(request, 'principal.html')