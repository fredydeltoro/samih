from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth.models import User, Group
from django.db import models

from apps.catalogos.estadisticos.especialidades.models import Especialidad
from apps.catalogos.estadisticos.geograficos.models import Nacionalidad, Entidad
from apps.catalogos.estadisticos.unidadesmedicas.models import UnidadMedica
from apps.catalogos.institucionales.turnos.models import Turno
from apps.catalogos.institucionales.tipoplazas.models import TipoPlaza
from apps.catalogos.institucionales.servicios.models import Servicio

class ProfesionalSalud(models.Model):

	GENERO = (('Femenino','Femenino'),('Masculino','Masculino'),)

	notrab = models.CharField(max_length=20, primary_key=True)
	usuario = models.OneToOneField(settings.AUTH_USER_MODEL, null=True, blank=True) #quitar null y blank
	nombre = models.CharField(max_length=250)
	apaterno = models.CharField(max_length=250)
	amaterno = models.CharField(max_length=250)
	curp = models.CharField(max_length=18)
	rfc = models.CharField(max_length=13)
	fecha_nac = models.DateField(null=True, blank=True) #quitar null y blank
	tel_celular = models.CharField(max_length=10, null=True, blank=True) #quitar null y blank
	tel_casa = models.CharField(max_length=10, null=True, blank=True)
	tel_consul = models.CharField(max_length=10, null=True, blank=True)
	turno = models.ForeignKey(Turno)
	servicio = models.ForeignKey(Servicio, null=True, blank=True)
	grupo = models.ForeignKey(Group, null=True, blank=True)
	especialidad1 = models.ForeignKey(Especialidad, related_name='especialidad1', null=True, blank=True)
	ced_prof1 = models.CharField(max_length=20, null=True, blank=True)
	especialidad2 = models.ForeignKey(Especialidad, related_name='especialidad2', null=True, blank=True)
	ced_prof2 = models.CharField(max_length=20, null=True, blank=True)
	especialidad3 = models.ForeignKey(Especialidad, related_name='especialidad3', null=True, blank=True)
	ced_prof3 = models.CharField(max_length=20, null=True, blank=True)
	cod_pues = models.ForeignKey('CodigoPuesto', null=True, blank=True)
	funcion_real = models.CharField(max_length=250, null=True, blank=True)
	fecha_ing = models.DateField(null=True, blank=True)
	tipo_plaza = models.ForeignKey(TipoPlaza)
	sexo = models.CharField(max_length=10, choices=GENERO)
	nacionalidad = models.ForeignKey(Nacionalidad, default='223')
	entidad = models.ForeignKey(Entidad, default='22')
	unidad_adscripcion = models.ForeignKey(UnidadMedica, default='QTSSA012935')
	comedor = models.BooleanField(default=False)
	cons_ext = models.BooleanField(default=False)
	receta = models.BooleanField(default=False)
	foto = models.ImageField(upload_to='usuarios', null=True, blank=True)

	class Meta:
		ordering = ('nombre',)

	def __unicode__(self):
		return self.nombre + ' ' + self.apaterno + ' ' + self.amaterno


class CodigoPuesto(models.Model):
	codigo = models.CharField(max_length=50,primary_key=True)
	nombre = models.CharField(max_length=255)

	def __unicode__(self):
		return self.codigo + ' - ' + self.nombre