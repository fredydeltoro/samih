from django.db.models import Q
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.views.generic import TemplateView, DetailView

from apps.catalogos.medicos.cies.models import Cie10
from apps.catalogos.medicos.catcauses.models import CatalogoCAUSES
from apps.servicios.administrativos.recursos_humanos.padronprofsalud.models import ProfesionalSalud

class InicioView(TemplateView):

	template_name = 'inicio.html'
	def get(self, request, *args, **kwargs):
		busqueda = request.GET.get('buscar','')
		if busqueda:
			qset = (
				Q(clave__icontains = busqueda) |
				Q(causes__clave__icontains = busqueda) |
				Q(nombre__icontains = busqueda)
			)
			resultados = Cie10.objects.filter(qset)
		else:
			resultados = []
		return render_to_response('inicio.html',{'diagnosticos':resultados,'busqueda':busqueda},context_instance=RequestContext(request))


class CausesView(DetailView):

	template_name = 'causes.html'
	model = CatalogoCAUSES


class PrincipalView(TemplateView):

	template_name = 'principal.html'

	def get_context_data(self, **kwargs):
	    context = super(PrincipalView, self).get_context_data(**kwargs)
	    context['usuario'] = ProfesionalSalud.objects.filter(usuario=self.request.user)
	    return context