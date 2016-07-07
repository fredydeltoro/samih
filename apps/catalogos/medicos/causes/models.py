#encoding:utf-8
from __future__ import unicode_literals

from django.db import models

class Causes(models.Model):
	""" Catalogo de CAUSES """
	clave = models.CharField(max_length=4)
	nombre = models.CharField(max_length=255)
	descripcion = models.CharField(max_length=255, null=True, blank=True)
	atenciones = models.ManyToManyField('AtencionIncluida', blank=True)
	intervenciones = models.ForeignKey('Intervencion', null=True, blank=True)

	def __unicode__(self):
		return '(' + str(self.clave) + ') ' + self.nombre

	def __str__(self):
		return '(' + str(self.clave) + ') ' + self.nombre


class AtencionIncluida(models.Model):
	""" Atenciones Incluidas en CAUSES """

	TipoCober = (('Área','Área'),('Insumo','Insumo'),)

	nombre = models.CharField(max_length=255)
	tipo = models.CharField(max_length=8, choices=TipoCober)

	def __unicode__(self):
		return self.nombre


class Intervencion(models.Model):
	""" Intervenciones en CAUSES """
	nombre = models.CharField(max_length=255)

	def __unicode__(self):
		return self.nombre
		

class TabuladorCauses(models.Model):
	""" Tabulador de CAUSES """
	causes = models.ForeignKey('Causes')
	costototal = models.DecimalField(max_digits=9, decimal_places=2)

	def __unicode__(self):
		return '(' + str(self.causes.clave) + ') ' + self.causes.nombre