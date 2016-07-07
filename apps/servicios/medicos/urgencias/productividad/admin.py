from django.contrib import admin
from .models import ProdUrgencias

@admin.register(ProdUrgencias)
class ProdUrgenciasAdmin(admin.ModelAdmin):
	pass