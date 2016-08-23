from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.principal, name='principal'),
	url(r'^pre-prueba/VIH/$', views.pre_prueba_vih, name='pre_prueba_vih')
]