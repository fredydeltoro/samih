from django.contrib import admin

from .models import Nacionalidad, Entidad, Municipio

@admin.register(Nacionalidad)
class NacionalidadAdmin(admin.ModelAdmin):
	list_display = ('clave','nombre','iniciales',)

@admin.register(Entidad)
class EntidadAdmin(admin.ModelAdmin):
	list_display = ('clave','nombre',)

@admin.register(Municipio)
class MunicipioAdmin(admin.ModelAdmin):
	list_display = ('num_mun','nombre','entidad',)
	list_filter = ('entidad',)