from django.contrib import admin
from .models import SolicitudFarmacia, ItemSolFarm

class ItemFarmInline(admin.TabularInline):
	model = ItemSolFarm

@admin.register(SolicitudFarmacia)
class SolicitudFarmaciaAdmin(admin.ModelAdmin):
	list_display = ('receta','paciente','medico','tiposol','fecha_creacion',)
	list_filter = ('tiposol',)
	search_fields = ('receta','paciente',)
	inlines = (ItemFarmInline,)