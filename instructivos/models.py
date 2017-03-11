from __future__ import unicode_literals
from django.template.defaultfilters import slugify
from django.db import models
from tinymce.models import HTMLField

class Concepto(models.Model):
	titulo = models.CharField(max_length=80)
	imagen = models.ImageField(upload_to="conceptos/", blank=True, default="")
	slug   = models.SlugField()
	activo = models.BooleanField(default=False)

	def __unicode__(self):
		return self.titulo

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.titulo)
		super(Concepto, self).save(*args, **kwargs)	

class Material(models.Model):
	concepto  = models.ForeignKey(Concepto)
	nombre    = models.CharField(max_length=50)
	slug      = models.SlugField()
	imagen    = models.ImageField(upload_to="materiales/", blank=True, default="")
	video     = models.CharField(max_length=200, blank=True, default="", help_text='La url donde se encuentra el video para el streaming')
	contenido = HTMLField()
	activo = models.BooleanField(default=False)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name_plural = "Materiales"

class Pregunta(models.Model):	
	pregunta = models.CharField(max_length=140)
	opcion_a = models.CharField(max_length=40)
	opcion_b = models.CharField(max_length=40)
	opcion_c = models.CharField(max_length=40)
	opcion_d = models.CharField(max_length=40)

	opciones = (
	    ('opcion_a', 'A'),
		('opcion_b', 'B'),
		('opcion_c', 'C'),
		('opcion_d', 'D'),
	)
	opcion_correcta = models.CharField(max_length=8, choices=opciones, default="opcion_a")

	def __unicode__(self):
		return self.pregunta


class Examen(models.Model):
	preguntas = models.ManyToManyField(Pregunta)
	concepto  = models.OneToOneField(Concepto)
	activo = models.BooleanField(default=False)
	
	def __unicode__(self):
		return "Examen %s" % self.concepto.titulo

	class Meta:
		verbose_name_plural = "Examenes"
