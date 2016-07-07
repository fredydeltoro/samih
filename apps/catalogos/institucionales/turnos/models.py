from __future__ import unicode_literals

from django.db import models

class Turno(models.Model):
	nombre = models.CharField(max_length=250)

	def __unicode__(self):
		return self.nombre