# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from .models import Concepto, Material, Pregunta, Examen
from django.contrib.auth.mixins import LoginRequiredMixin

class CourseView(LoginRequiredMixin, View):
	"""
	Vista donde se muestran los conceptos y materiales, desde aqui se puede modificar la informacion
	"""
	login_url = '/login/'
	
	def get(self, request):
		conceptos  = Concepto.objects.all()
		materiales = Material.objects.all()
		ctx        = {"conceptos":conceptos, "materiales": materiales}
		template   = "manager/index.html"
		return render(request, template, ctx)


class AddConceptView(LoginRequiredMixin, TemplateView):
	"""
	Vista donde se puede agregar un concepto
	"""
	template_name = "manager/add_concept.html"
	login_url = '/login/'

	def get(self, request):
		return render(request, self.template_name)

	def post(self, request):
		ctx = {
			"mensaje": "Hola Mundo"
		}
		return render(request, self.template_name, ctx)