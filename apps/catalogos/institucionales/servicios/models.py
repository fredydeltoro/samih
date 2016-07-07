from __future__ import unicode_literals

from django.db import models

class Servicio(models.Model):
	nombre = models.CharField(max_length=250)

	def __unicode__(self):
		return self.nombre