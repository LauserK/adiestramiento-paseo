from django.shortcuts import render
from django.views.generic import View
from .models import Concepto, Material, Pregunta, Examen
from django.contrib.auth.mixins import LoginRequiredMixin

class CourseView(LoginRequiredMixin, View):
	"""
	Clase donde se muestran los conceptos y materiales, desde aqui se puede modificar la informacion
	"""
	login_url = '/login/'
	
	def get(self, request):
		conceptos  = Concepto.objects.all()
		materiales = Material.objects.all()
		ctx        = {"conceptos":conceptos, "materiales": materiales}
		template   = "manager/index.html"
		return render(request, template, ctx)