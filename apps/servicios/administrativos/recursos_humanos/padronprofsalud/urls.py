from django.conf.urls import url

from .views import IniciarSesionView, CerrarSesionView, RegistrarUsuarioView

urlpatterns = [
    url(r'^iniciarsesion/$',IniciarSesionView.as_view()),
	url(r'^cerrarsesion/$',CerrarSesionView.as_view()),
	url(r'^registrarusuario/$',RegistrarUsuarioView.as_view()),
]