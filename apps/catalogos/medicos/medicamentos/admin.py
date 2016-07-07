from django.contrib import admin

from .models import CuadroBasico, PresentacionMed

@admin.register(CuadroBasico)
class CuadroBasicoAdmin(admin.ModelAdmin):
	list_display = ('clave_farmacia','nombre','fecha_caducidad','lote','precio','farmacia','controlado',)
	list_editable = ('fecha_caducidad','lote','farmacia','controlado',)
	list_filter = ('farmacia','controlado',)
	search_fields = ('clave_farmacia','nombre',)


@admin.register(PresentacionMed)
class PresentacionMedAdmin(admin.ModelAdmin):
	list_display = ('clave','descripcion')
	search_fields = ('clave',)