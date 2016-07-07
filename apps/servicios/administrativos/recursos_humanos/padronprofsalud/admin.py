from django.contrib import admin

from .models import ProfesionalSalud, CodigoPuesto

@admin.register(ProfesionalSalud)
class ProfesionalSaludAdmin(admin.ModelAdmin):
	list_display = ('notrab','nombre','apaterno','amaterno','comedor','cons_ext',)
	list_filter = ('turno','tipo_plaza','cod_pues',)
	search_fields = ('notrab','apaterno','amaterno','curp','rfc',)


@admin.register(CodigoPuesto)
class CodigoPuestoAdmin(admin.ModelAdmin):
	list_display = ('codigo','nombre',)