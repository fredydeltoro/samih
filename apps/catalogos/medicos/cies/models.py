from django.db import models
from apps.catalogos.medicos.causes.models import Causes

class Cie9MC(models.Model):
	""" CIE9 MC """
	clave = models.CharField(max_length=20,primary_key=True,unique=True)
	nombre = models.CharField(max_length=500)
	cies = models.CharField(max_length=5,default='CIE9',editable=False)
	causes = models.ManyToManyField(Causes,related_name='cie9_causes')
	def __unicode__(self):
		return '(' + self.clave + ') ' + self.nombre

class Cie10(models.Model):
	""" CIE10 """
	clave = models.CharField(max_length=20,primary_key=True,unique=True)
	nombre = models.CharField(max_length=500)
	cies = models.CharField(max_length=5,default='CIE10',editable=False)
	capitulo = models.ForeignKey('Cie10Caps')
	causes = models.ManyToManyField(Causes,related_name='cie10_causes')
	def __unicode__(self):
		return '(' + self.clave + ') ' + self.nombre

class Cie10Caps(models.Model):
	""" Capitulos de CIE10 """
	capitulo = models.CharField(max_length=6,primary_key=True,unique=True)
	nombre = models.CharField(max_length=250)
	def __unicode__(self):
		return self.capitulo