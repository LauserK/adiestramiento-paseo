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
	"""
	Vista para editar un concepto
	"""
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
	"""
	Vista para agregar un material
	"""
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

class RemoveMaterialView(LoginRequiredMixin, View):
	"""
	Eliminar Material
	"""
	def get(self, request, materialSlug):
		material = get_object_or_404(Material, slug=materialSlug)
		material.delete()

		return redirect('/')

class RemoveConceptView(LoginRequiredMixin, View):
	"""
	Eliminar concepto
	"""
	def get(self, request, conceptSlug):
		concepto = get_object_or_404(Concepto, slug=conceptSlug)
		concepto.delete()

		return redirect('/')

class EditMaterialView(LoginRequiredMixin, TemplateView):
	"""
	Editar material
	"""
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

		return redirect('/')


"""EXAMENES"""

class ExamenView(View):
	template_name = "manager/examenes.html"

	def get(self, request):
		examenes  = Examen.objects.all().filter(activo=True)
		preguntas = Pregunta.objects.all()
		ctx = {
			"examenes": examenes,
			"preguntas": preguntas
		}
		return render(request, self.template_name, ctx)


class SingleExamenView(View):
	template_name = "manager/single_examenes.html"

	def get(self, request, examenSlug):
		preguntas = Pregunta.objects.all()
		examen    = get_object_or_404(Examen, pk=examenSlug)
		ctx = {
			"preguntas":preguntas,
			"examen":examen
		}
		return render(request, self.template_name, ctx)


class AddExamenView(View):
	"""
	Vista para crear un nuevo examen
	"""
	template_name = "manager/add_examenes.html"

	def get(self, request):
		conceptos = Concepto.objects.filter(activo=True)
		ctx = {
			"conceptos": conceptos
		}
		return render(request, self.template_name, ctx)

	def post(self, request):
		concepto   = get_object_or_404(Concepto, pk=request.POST.get('concepto'))
		activo     = request.POST.get('activo')

		if activo == "on":
			activo = True
		else:
			activo = False

		nuevo_examen    = Examen()
		nuevo_examen.concepto = concepto
		nuevo_examen.activo   = activo
		nuevo_examen.save()

		return redirect("/manager/examen")


class EditExamenView(View):
	template_name = "manager/edit_examenes.html"

	def get(self, request, examenSlug):
		examen = get_object_or_404(Examen, id=examenSlug)
		conceptos = Concepto.objects.filter(activo=True)
		ctx = {
			"examen": examen,
			"conceptos": conceptos
		}
		return render(request, self.template_name, ctx)

	def post(self, request, examenSlug):
		examen          = get_object_or_404(Examen, pk=examenSlug)
		examen.concepto = Concepto.objects.get(pk=request.POST.get('concepto'))
		activo          = request.POST.get('activo')
		if activo == "on":
			activo = True
		else:
			activo = False
		examen.activo   = activo
		examen.save()

		return redirect('/manager/examen')

class RemoveExamenView(View):
	template_name = "manager/remove_examenes.html"

	def get(self, request, examenSlug):
		examen = get_object_or_404(Examen, pk=examenSlug)
		examen.delete()

		return redirect('/manager/examen')


"""
Preguntas
"""
class AddPregunta(View):
	template_name = "manager/add_pregunta.html"

	def get(self, request, examenSlug):
		examen = get_object_or_404(Examen, pk=examenSlug)
		ctx = {
			"examen": examen
		}
		return render(request, self.template_name, ctx)

	def post(self, request, examenSlug):
		pass