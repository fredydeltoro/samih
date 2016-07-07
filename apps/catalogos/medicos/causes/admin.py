from django.contrib import admin

from .models import  Causes, AtencionIncluida, TabuladorCauses, Intervencion

@admin.register(Causes)
class CausesAdmin(admin.ModelAdmin):
	list_display = ('clave', 'nombre','descripcion','intervenciones')
	list_editable = ('intervenciones',)

@admin.register(AtencionIncluida)
class AtencionIncluidaAdmin(admin.ModelAdmin):
	list_display = ('nombre',)

@admin.register(TabuladorCauses)
class TabuladorCausesAdmin(admin.ModelAdmin):
	list_display = ('causes','costototal',)

@admin.register(Intervencion)
class IntervencionAdmin(admin.ModelAdmin):
	list_display = ('id','nombre',)