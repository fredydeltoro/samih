from django.contrib import admin

from .models import UnidadMedica

@admin.register(UnidadMedica)
class UnidadMedicaAdmin(admin.ModelAdmin):
	list_display = ('clues','nombre',)