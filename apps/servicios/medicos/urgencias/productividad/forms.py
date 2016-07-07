from django import forms

class MesesForm(forms.Form):
	mes = forms.CharField(max_length=2,
		  widget=forms.TextInput(attrs={
		'class' : 'form-control',
		'placeholder' : 'Mes'
		}))