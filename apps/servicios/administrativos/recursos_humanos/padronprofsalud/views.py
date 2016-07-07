from django.contrib.auth import authenticate, login, logout
from django.views.generic import FormView, RedirectView

from .forms import IniciarSesionForm, RegistroUsuarioForm

class IniciarSesionView(FormView):

	form_class = IniciarSesionForm
	template_name = 'iniciar_sesion.html'
	success_url = '/principal/'

	def form_valid(self, form):
		user = authenticate(username=form.cleaned_data['username'], 
							password=form.cleaned_data['password'])
		if user is not None:
			if user.is_active:
				login(self.request, user)
		return super(IniciarSesionView,self).form_valid(form)


class CerrarSesionView(RedirectView):
	url = '/iniciarsesion/'

	def get(self,request, *args, **kwargs):
		logout(request)
		return super(CerrarSesionView, self).get(request,*args,**kwargs)


class RegistrarUsuarioView(FormView):

	form_class = RegistroUsuarioForm
	template_name = 'registrar_usuario.html'
	success_url = '/registrarusuario/'

	def form_valid(self, form):
		form.save()
		return super(RegistrarUsuarioView, self).form_valid(form)
