# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import View, TemplateView
from .models import Concepto, Material, Pregunta, Examen
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.db import IntegrityError

class CourseView(LoginRequiredMixin, View):
	"""
	Vista donde se muestran los conceptos y materiales,
	desde aqui se puede modificar la informacion
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
	"""
	Mostrar lista de examenes
	"""
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
	"""
	Mostrar examen y pregunta individual
	"""
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
		materiales = Material.objects.filter(activo=True)
		ctx = {
			"materiales": materiales
		}
		return render(request, self.template_name, ctx)

	def post(self, request):
		material   = get_object_or_404(Material, pk=request.POST.get('material'))
		activo     = request.POST.get('activo')
		materiales = Material.objects.filter(activo=True)

		if activo == "on":
			activo = True
		else:
			activo = False

		try:
			nuevo_examen          = Examen()
			nuevo_examen.material = material
			nuevo_examen.activo   = activo
			nuevo_examen.save()
		except IntegrityError:
			ctx = {
				"materiales": materiales,
				"mensaje": "¡Ya existe un examen para el instructivo asociado!"
			}
			return render(request, self.template_name, ctx)


		return redirect("/manager/examen")


class EditExamenView(View):
	"""
	Editar examen (Solo el concepto y si esta activo)
	"""
	template_name = "manager/edit_examenes.html"

	def get(self, request, examenSlug):
		examen = get_object_or_404(Examen, id=examenSlug)
		materiales = Material.objects.filter(activo=True)
		ctx = {
			"examen": examen,
			"materiales": materiales
		}
		return render(request, self.template_name, ctx)

	def post(self, request, examenSlug):
		examen          = get_object_or_404(Examen, pk=examenSlug)
		examen.material = Material.objects.get(pk=request.POST.get('material'))
		activo          = request.POST.get('activo')
		if activo == "on":
			activo = True
		else:
			activo = False
			
		try:
			examen.activo   = activo
			examen.save()
		except IntegrityError:
			ctx = {
				"materiales": materiales,
				"mensaje": "¡Ya existe un examen para el instructivo asociado!"
			}
			return render(request, self.template_name, ctx)

		return redirect('/manager/examen')

class RemoveExamenView(View):
	"""
	Eliminar examenes
	"""
	template_name = "manager/remove_examenes.html"

	def get(self, request, examenSlug):
		examen = get_object_or_404(Examen, pk=examenSlug)
		examen.delete()

		return redirect('/manager/examen')


"""
Preguntas
"""
class AddPregunta(View):
	"""
	Agregar pregunta a un examen
	"""
	template_name = "manager/add_pregunta.html"

	def get(self, request, examenSlug):
		examen = get_object_or_404(Examen, pk=examenSlug)
		ctx = {
			"examen": examen
		}
		return render(request, self.template_name, ctx)

	def post(self, request, examenSlug):
		examen = get_object_or_404(Examen, pk=examenSlug)

		# FORM DATA
		pregunta    = request.POST.get('pregunta').encode("utf-8")
		opcion_a    = request.POST.get('opcion_a').encode("utf-8")
		opcion_b    = request.POST.get('opcion_b').encode("utf-8")
		opcion_c    = request.POST.get('opcion_c').encode("utf-8")
		opcion_d    = request.POST.get('opcion_d').encode("utf-8")
		correcta    = request.POST.get('opcion_correcta')
		ilustracion = request.FILES.get('ilustracion')

		if pregunta == None or pregunta == "":
			ctx = {
				"examen": examen,
				"pregunta": pregunta,
				"opcion_a": opcion_a,
				"opcion_b": opcion_b,
				"opcion_c": opcion_c,
				"opcion_d": opcion_d,
				"correcta": correcta,
				"mensaje": "El enunciado no puede estar vacío"
			}
			return render(request, self.template_name, ctx)

		if opcion_a == None or opcion_a == "" or opcion_b == None or opcion_b == "" or opcion_c == None or opcion_c == "" or opcion_d == None or opcion_d == "":
			ctx = {
				"examen": examen,
				"pregunta": pregunta,
				"opcion_a": opcion_a,
				"opcion_b": opcion_b,
				"opcion_c": opcion_c,
				"opcion_d": opcion_d,
				"correcta": correcta,
				"examen": examen,
				"mensaje": "Algunas respuestas estan vacias"
			}
			return render(request, self.template_name, ctx)


		nueva_pregunta                  = Pregunta()
		nueva_pregunta.pregunta         = pregunta
		nueva_pregunta.opcion_a         = opcion_a
		nueva_pregunta.opcion_b         = opcion_b
		nueva_pregunta.opcion_c         = opcion_c
		nueva_pregunta.opcion_d         = opcion_d
		nueva_pregunta.opcion_correcta  = correcta

		if ilustracion is not None:
			nueva_pregunta.ilustracion  = ilustracion

		nueva_pregunta.save()

		examen.preguntas.add(nueva_pregunta)


		return redirect(reverse('single-examenes', kwargs={'examenSlug': examen.pk}))


class EditPregunta(View):
	"""
	Editar pregunta
	"""
	template_name = "manager/add_pregunta.html"

	def get(self, request, examenSlug, preguntaId):
		examen = get_object_or_404(Examen, pk=examenSlug)
		pregunta = get_object_or_404(Pregunta, pk=preguntaId)
		ctx = {
			"examen": examen,
			"pregunta": pregunta.pregunta,
			"opcion_a": pregunta.opcion_a,
			"opcion_b": pregunta.opcion_b,
			"opcion_c": pregunta.opcion_c,
			"opcion_d": pregunta.opcion_d,
			"correcta": pregunta.opcion_correcta,
			"ilustracion": pregunta.get_image,
			"editar": request.GET.get('editar')
		}
		return render(request, self.template_name, ctx)

	def post(self, request, examenSlug, preguntaId):
		examen = get_object_or_404(Examen, pk=examenSlug)

		# FORM DATA
		pregunta    = request.POST.get('pregunta').encode("utf-8")
		opcion_a    = request.POST.get('opcion_a').encode("utf-8")
		opcion_b    = request.POST.get('opcion_b').encode("utf-8")
		opcion_c    = request.POST.get('opcion_c').encode("utf-8")
		opcion_d    = request.POST.get('opcion_d').encode("utf-8")
		correcta    = request.POST.get('opcion_correcta')
		ilustracion = request.FILES.get('ilustracion')

		if pregunta == None or pregunta == "":
			ctx = {
				"examen": examen,
				"pregunta": pregunta,
				"opcion_a": opcion_a,
				"opcion_b": opcion_b,
				"opcion_c": opcion_c,
				"opcion_d": opcion_d,
				"correcta": correcta,
				"mensaje": "El enunciado no puede estar vacío"
			}
			return render(request, self.template_name, ctx)

		if opcion_a == None or opcion_a == "" or opcion_b == None or opcion_b == "" or opcion_c == None or opcion_c == "" or opcion_d == None or opcion_d == "":
			ctx = {
				"examen": examen,
				"pregunta": pregunta,
				"opcion_a": opcion_a,
				"opcion_b": opcion_b,
				"opcion_c": opcion_c,
				"opcion_d": opcion_d,
				"correcta": correcta,
				"examen": examen,
				"mensaje": "Algunas respuestas estan vacias"
			}
			return render(request, self.template_name, ctx)


		edit_pregunta                  = get_object_or_404(Pregunta, pk=preguntaId)
		edit_pregunta                  = Pregunta.objects.get(pk=preguntaId)
		edit_pregunta.pregunta         = pregunta
		edit_pregunta.opcion_a         = opcion_a
		edit_pregunta.opcion_b         = opcion_b
		edit_pregunta.opcion_c         = opcion_c
		edit_pregunta.opcion_d         = opcion_d
		edit_pregunta.opcion_correcta  = correcta

		if ilustracion is not None:
			edit_pregunta.ilustracion  = ilustracion

		edit_pregunta.save()

		return redirect(reverse('single-examenes', kwargs={'examenSlug': examen.pk}))
