from django.contrib import admin
from .models import Concepto, Material, Pregunta, Examen, Orden

admin.site.site_header = 'ADIESTRAMIENTO PASEO78'

@admin.register(Orden)
class OrdenAdmin(admin.ModelAdmin):
	pass

@admin.register(Concepto)
class ConceptoAdmin(admin.ModelAdmin):
	pass

@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
	pass

@admin.register(Pregunta)
class PreguntaAdmin(admin.ModelAdmin):
	pass

@admin.register(Examen)
class ExamenAdmin(admin.ModelAdmin):
	pass
