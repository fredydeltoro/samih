from __future__ import unicode_literals

from django.db import models
from apps.catalogos.medicos.causes.models import Causes
from apps.catalogos.medicos.cies.models import Cie10, Cie9MC
from apps.catalogos.medicos.medicamentos.models import CuadroBasico

class CatalogoCAUSES(models.Model):
	causes = models.OneToOneField(Causes, related_name='causes_cat')
	diags = models.ManyToManyField(Cie10, related_name='diags_cat', blank=True)
	procs = models.ManyToManyField(Cie9MC, related_name='procs_cat', blank=True)
	meds = models.ManyToManyField(CuadroBasico, related_name='meds_cat', blank=True)

	def __unicode__(self):
		return self.causes.clave + ' - ' + self.causes.nombre