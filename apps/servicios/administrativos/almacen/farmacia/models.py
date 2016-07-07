from __future__ import unicode_literals

from django.db import models
from django.conf import settings
from apps.servicios.administrativos.recursos_humanos.padronprofsalud.models import ProfesionalSalud
from apps.catalogos.medicos.medicamentos.models import CuadroBasico

class SolicitudFarmacia(models.Model):
	""" Solicitud de Farmacia """
	
	tipoSol = (('venta','venta'),('segpop','segpop'),('medcontrolado','medcontrolado'),)

	usuario = models.ForeignKey(settings.AUTH_USER_MODEL)
	receta = models.CharField(max_length=8)
	receta2 = models.CharField(max_length=8, null=True, blank=True)
	poliza_segpop = models.CharField(max_length=12, null=True, blank=True)
	paciente = models.CharField(max_length=255)
	medico = models.ForeignKey(ProfesionalSalud)
	tiposol = models.CharField(max_length=15, choices=tipoSol)
	fecha_creacion = models.DateTimeField(auto_now_add=True)
	fecha_modificacion = models.DateTimeField(auto_now=True)

	def __unicode__(self):
		return self.receta + ' - ' + self.paciente

	@models.permalink
	def get_absolute_url(self):
		return('solfarm' + self.tiposol, [self.pk])


class ItemSolFarm(models.Model):
	""" Medicamento de la Solicitud de Farmacia """
	solfarm = models.ForeignKey('SolicitudFarmacia')
	medicamento = models.ForeignKey(CuadroBasico)
	cantidad_surtida = models.PositiveIntegerField()
	cantidad_recetada = models.PositiveIntegerField()
	fecha_creacion = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return str(self.solfarm.id) + ' - ' + self.medicamento.nombre