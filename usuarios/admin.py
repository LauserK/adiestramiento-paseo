from django.contrib import admin
from .models import UserProfile, ExamenAprobado

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
	filter_horizontal = ('materiales_aprobados',)

@admin.register(ExamenAprobado)
class ExamenAprobadoAdmin(admin.ModelAdmin):
	pass
