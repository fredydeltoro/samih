from django.db import models

class ProdUrgencias(models.Model):
	medico = models.CharField(max_length=8)
	nombre = models.CharField(max_length=250)
	turno = models.CharField(max_length=20, blank=True, null=True)
	servicio = models.CharField(max_length=250, blank=True, null=True)
	fecha_hora_ing = models.DateTimeField()
	fecha_hora_mod = models.DateTimeField()

	def __unicode__(self):
		return self.medico + ' - ' +self.nombre