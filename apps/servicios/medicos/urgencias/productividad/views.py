from django.db.models import Count
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView
from .models import ProdUrgencias
from .forms import MesesForm

class ProdUrg(TemplateView):

	template_name = 'productividad_urg.html'
	form_class = MesesForm

	def get(self, request, *args, **kwargs):
		mes = request.GET.get('mes','')
		anio = 2015
		if mes:
			matutino = ProdUrgencias.objects.values('medico','nombre').filter(fecha_hora_ing__month = mes, fecha_hora_ing__year = anio, servicio = 'URGENCIAS', turno = 'MATUTINO').annotate(total=Count('medico')).order_by('medico')
			vespertino = ProdUrgencias.objects.values('medico','nombre').filter(fecha_hora_ing__month = mes, fecha_hora_ing__year = anio, servicio = 'URGENCIAS', turno = 'VESPERTINO').annotate(total=Count('medico')).order_by('medico')
			noct_a = ProdUrgencias.objects.values('medico','nombre').filter(fecha_hora_ing__month = mes, fecha_hora_ing__year = anio, servicio = 'URGENCIAS', turno = 'NOCTURNO A').annotate(total=Count('medico')).order_by('medico')
			noct_b = ProdUrgencias.objects.values('medico','nombre').filter(fecha_hora_ing__month = mes, fecha_hora_ing__year = anio, servicio = 'URGENCIAS', turno = 'NOCTURNO B').annotate(total=Count('medico')).order_by('medico')
			esp_dia = ProdUrgencias.objects.values('medico','nombre').filter(fecha_hora_ing__month = mes, fecha_hora_ing__year = anio, servicio = 'URGENCIAS', turno = 'ESPECIAL DIA').annotate(total=Count('medico')).order_by('medico')
			esp_noct = ProdUrgencias.objects.values('medico','nombre').filter(fecha_hora_ing__month = mes, fecha_hora_ing__year = anio, servicio = 'URGENCIAS', turno = 'ESPECIAL NOCTURNO').annotate(total=Count('medico')).order_by('medico')
		else:
			matutino = []
			vespertino = []
			noct_a = []
			noct_b = []
			esp_dia = []
			esp_noct = []
		return render_to_response('productividad_urg.html',{'mes':mes,'anio':anio,'matutino':matutino,'vespertino':vespertino,
								  'noct_a': noct_a,'noct_b': noct_b,'esp_dia': esp_dia,'esp_noct': esp_noct,},
								  context_instance=RequestContext(request))