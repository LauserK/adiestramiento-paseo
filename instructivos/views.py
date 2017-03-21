# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView
from .models import Concepto, Material, Pregunta, Examen
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse

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
		nuevo_concepto.save()
			
		return redirect('/')

class EditConceptView(LoginRequiredMixin, TemplateView):
	template_name = "manager/edit_concept.html"
	login_url = '/login/'	

	def get(self, request, conceptSlug):
		concepto = get_object_or_404(Concepto, slug=conceptSlug)
		ctx = {
			"concepto": concepto
		}
		return render(request, self.template_name, ctx)

	def post(self, request, conceptSlug):
		mensaje = ""
		titulo  = request.POST.get("titulo")
		activo  = request.POST.get("activo")

		if titulo is None or titulo == "":
			mensaje = "¡El título no puede estar vacio!"
			return render(request, self.template_name, {"mensaje": mensaje})

		if activo == "on":
			activo = True
		else:
			activo = False

		nuevo_concepto        = Concepto.objects.get(slug=conceptSlug)
		nuevo_concepto.titulo = titulo
		nuevo_concepto.activo = activo
		nuevo_concepto.save()
			
		return redirect('/')

class AddMaterialView(LoginRequiredMixin, TemplateView):
	template_name = "manager/add_material.html"
	login_url = "/login/"

	def get(self, request, conceptSlug):
		concepto = get_object_or_404(Concepto, slug=conceptSlug)

		ctx = {
			"concepto": concepto
		}
		return render(request, self.template_name, ctx)

	def post(self, request, conceptSlug):
		mensaje    = ""
		concepto   = get_object_or_404(Concepto, slug=conceptSlug)
		nombre     = request.POST.get('nombre')
		imagen     = request.FILES.get('imagen')
		video      = request.FILES.get('video')
		contenido  = request.POST.get('contenido')
		activo     = request.POST.get('activo')

		if activo == "on":
			activo = True
		else:
			activo = False
		
		if nombre is None or nombre == "":
			mensaje = "¡El nombre no puede estar vacio!"
			return render(request, self.template_name, {"mensaje": mensaje})

		nuevo_material           = Material()
		nuevo_material.concepto  = concepto
		nuevo_material.nombre    = nombre
		nuevo_material.contenido = contenido
		nuevo_material.activo    = activo

		if video is not None:
			nuevo_material.video  = video

		if imagen is not None:
			if ".jpg" in imagen.name or ".png" in imagen.name:
				nuevo_material.imagen = imagen

		nuevo_material.save()

		return redirect('/')

class RemoveMaterialView(View):
	def get(self, request, materialSlug):
		material = get_object_or_404(Material, slug=materialSlug)
		material.delete()

		return redirect('/')

class RemoveConceptView(View):
	def get(self, request, conceptSlug):
		concepto = get_object_or_404(Concepto, slug=conceptSlug)
		concepto.delete()

		return redirect('/')

class EditMaterialView(LoginRequiredMixin, TemplateView):
	template_name = "manager/edit_material.html"
	login_url = "/login/"

	def get(self, request, materialSlug):		
		material = get_object_or_404(Material, slug=materialSlug)

		ctx = {
			"concepto": material.concepto,
			"material": material
		}

		return render(request, self.template_name, ctx)

	def post(self, request, materialSlug):
		mensaje    = ""
		nombre     = request.POST.get('nombre')		
		video      = request.FILES.get('video')
		contenido  = request.POST.get('contenido')
		activo     = request.POST.get('activo')

		if activo == "on":
			activo = True
		else:
			activo = False
		
		if nombre is None or nombre == "":
			mensaje = "¡El nombre no puede estar vacio!"
			return render(request, self.template_name, {"mensaje": mensaje})

		nuevo_material           = Material.objects.get(slug=materialSlug)
		nuevo_material.nombre    = nombre
		nuevo_material.contenido = contenido
		nuevo_material.activo    = activo

		if video is not None:
			nuevo_material.video  = video

		nuevo_material.save()

		return HttpResponse('<script type="text/javascript">window.close()</script>')