from django.contrib import admin

from .models import TipoPlaza

@admin.register(TipoPlaza)
class TipoPlazaAdmin(admin.ModelAdmin):
	list_display = ('id','nombre',)