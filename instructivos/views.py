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
		mensaje = ""
		titulo  = request.POST.get("titulo")
		activo  = request.POST.get("activo")
		imagen  = request.FILES.get("imagen")

		if titulo is None or titulo == "":
			mensaje = "¡El título no puede estar vacio!"
			return render(request, self.template_name, {"mensaje": mensaje})

		if activo == "on":
			activo = True
		else:
			activo = False

		nuevo_concepto        = Concepto()
		nuevo_concepto.titulo = titulo
		nuevo_concepto.activo = activo
		if imagen is not None:
			nuevo_concepto.imagen = imagen
			
		nuevo_concepto.save()
			
		return redirect('/')

class EditConceptView(LoginRequiredMixin, TemplateView):
	template_name = "manager/add_concept.html"
	login_url = '/login/'

class AddMaterialView(LoginRequiredMixin, TemplateView):
	template_name = "manager/add_material.html"
	login_url = "/login/"

	def get(self, request, conceptSlug):
		concepto = Concepto.objects.get(slug=conceptSlug)

		ctx = {
			"concepto": concepto
		}
		return render(request, self.template_name, ctx)

