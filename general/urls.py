from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^login/$', views.login, name='login'),
	url(r'^crear/usuario/$', views.crear_usuario, name='crear_usuario'),
]