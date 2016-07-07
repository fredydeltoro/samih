from django import forms
from django.forms.models import inlineformset_factory

from .models import SolicitudFarmacia, ItemSolFarm
from apps.servicios.administrativos.recursos_humanos.padronprofsalud.models import ProfesionalSalud
from apps.catalogos.medicos.medicamentos.models import CuadroBasico

class SolicitudFarmaciaForm(forms.ModelForm):
	class Meta:
		model = SolicitudFarmacia
		fields = ('receta','receta2','poliza_segpop','paciente','medico',)
		widgets = {
			'receta': forms.TextInput(attrs =
				{
					'class': 'form-control',
					'placeholder': 'No. de Receta',
				}),
			'receta2': forms.TextInput(attrs =
				{
					'class': 'form-control',
					'placeholder': 'No. de Receta',
				}),
			'poliza_segpop': forms.TextInput(attrs =
				{
					'class': 'form-control',
					'placeholder': 'No. de Poliza',
				}),
			'paciente': forms.TextInput(attrs =
				{
					'class': 'form-control',
					'placeholder': 'Nombre del Paciente',
					'size': '107',
				}),
		}
	medico = forms.ModelChoiceField(queryset=ProfesionalSalud.objects.filter(receta=1), widget=forms.Select(attrs = 
		{
			'class': 'form-control',
		}))


class ItemSolFarmForm(forms.ModelForm):
	class Meta:
		model = ItemSolFarm
		fields = ('cantidad_surtida','cantidad_recetada','medicamento',)
		widgets = {
			'cantidad_surtida': forms.TextInput(attrs =
				{
					'class': 'form-control',
					'placeholder': 'Cantidad',
				}),
			'cantidad_recetada': forms.TextInput(attrs =
				{
					'class': 'form-control',
					'placeholder': 'Cantidad',
				}),
		}
	medicamento = forms.ModelChoiceField(queryset=CuadroBasico.objects.filter(farmacia=1,controlado=0), widget=forms.Select(attrs = 
		{
			'class': 'form-control',
		}))


ItemSolFarmFormSet = inlineformset_factory(
	SolicitudFarmacia,
	ItemSolFarm,
	extra = 0,
	min_num = 1,
	form = ItemSolFarmForm
)

class ItemSolFarmMedControladoForm(forms.ModelForm):
	class Meta:
		model = ItemSolFarm
		fields = ('cantidad_surtida','medicamento',)
		widgets = {
			'cantidad_surtida': forms.TextInput(attrs =
				{
					'class': 'form-control',
					'placeholder': 'Cantidad',
				}),
			'cantidad_recetada': forms.TextInput(attrs =
				{
					'class': 'form-control',
					'placeholder': 'Cantidad',
				}),
		}
	medicamento = forms.ModelChoiceField(queryset=CuadroBasico.objects.filter(farmacia=1,controlado=1), widget=forms.Select(attrs = 
		{
			'class': 'form-control',
		}))


ItemSolFarmMedControladoFormSet = inlineformset_factory(
	SolicitudFarmacia,
	ItemSolFarm,
	extra = 0,
	min_num = 1,
	form = ItemSolFarmMedControladoForm
)