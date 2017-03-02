from django.shortcuts import render
from django.views.generic import View
from .models import Concepto, Material, Pregunta, Examen

class CourseView(View):
	"""
	Clase donde se muestran los conceptos y materiales, desde aqui se puede modificar la informacion
	"""
	def get(self, request):
		conceptos  = Concepto.objects.all()
		materiales = Material.objects.all()
		ctx        = {"conceptos":conceptos, "materiales": materiales}
		template   = "manager/index.html"
		return render(request, template, ctx)