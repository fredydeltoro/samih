#encoding:utf-8
from __future__ import unicode_literals

from django.db import models
from apps.catalogos.medicos.causes.models import Causes

class CuadroBasico(models.Model):
	""" Medicamentos del Cuadro Básico """
	clave = models.CharField(max_length=20)
	clave_farmacia = models.CharField(max_length=8)
	nombre = models.CharField(max_length=255)
	descripcion = models.CharField(max_length=255, null=True, blank=True)
	presentacion = models.ForeignKey('PresentacionMed', null=True, blank=True)
	fecha_caducidad = models.DateField(null=True, blank=True)
	lote = models.CharField(max_length=20, null=True, blank=True)
	precio = models.DecimalField(max_digits=9, decimal_places=2, null=True, blank=True)
	causes = models.ManyToManyField(Causes,related_name='cuadrobasico_causes')
	farmacia = models.BooleanField(default=False)
	controlado = models.BooleanField(default=False)

	class Meta:
		ordering = ('nombre',)

	def __unicode__(self):
		return self.nombre


class PresentacionMed(models.Model):
	""" Presentación del Medicamento """
	clave = models.CharField(max_length=8, primary_key=True)
	descripcion = models.CharField(max_length=255)

	def __unicode__(self):
		return self.clave