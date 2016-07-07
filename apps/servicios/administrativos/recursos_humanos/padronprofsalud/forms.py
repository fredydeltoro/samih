#encoding:utf-8
from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class IniciarSesionForm(forms.Form):
	username = forms.CharField(max_length=30,
		widget=forms.TextInput(attrs=
			{
				'class' : 'form-control',
				'placeholder' : 'Nombre de usuario'
			}))
	password = forms.CharField(max_length=30,
		widget=forms.TextInput(attrs=
			{
				'type' : 'password',
				'class' : 'form-control',
				'placeholder' : 'Contraseña'
			}))


class RegistroUsuarioForm(UserCreationForm):
	email = forms.EmailField()

	class Meta:
		model = User
		fields = ('username', 'email')