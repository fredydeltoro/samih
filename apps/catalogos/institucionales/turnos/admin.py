from django.contrib import admin

from .models import Turno

@admin.register(Turno)
class TurnoAdmin(admin.ModelAdmin):
	list_display = ('id','nombre',)