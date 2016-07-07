from __future__ import unicode_literals

from django.db import models

from apps.catalogos.estadisticos.geograficos.models import Municipio

class UnidadMedica(models.Model):
	JURIS = (('01','01'),('02','02'),('03','03'),('04','04'),('05','05'),)
	clues = models.CharField(max_length=20, primary_key=True, unique=True)
	nombre = models.CharField(max_length=250)
	jurisdiccion = models.CharField(max_length=2, choices=JURIS)
	municipio = models.ForeignKey(Municipio)

	def __unicode__(self):
		return self.clues + ' - ' + self. nombre