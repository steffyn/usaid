from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.principal, name='principal'),
	url(r'^pre-prueba/VIH/$', views.pre_prueba_vih, name='pre_prueba_vih'),
	url(r'^prueba/VIH/$', views.prueba_vih, name='prueba_vih'),
	url(r'^post-prueba/VIH/$', views.post_prueba_vih, name='post_prueba_vih'),
	url(r'^listado/asistencia/$', views.listado_asistencia, name='listado_asistencia'),
	url(r'^clinica/$', views.boleta_clinica, name='boleta_clinica'),
	url(r'^ajax/$', views.ajax, name='ajax'),
]