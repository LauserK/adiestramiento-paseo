from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from django.template.defaultfilters import slugify
from froala_editor.fields import FroalaField
from django.conf import settings
import datetime
from django.conf import settings

class Concepto(models.Model):
	titulo = models.CharField(max_length=80)
	slug   = models.SlugField()
	activo = models.BooleanField(default=False)

	def __unicode__(self):
		return self.titulo

	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.titulo)
		super(Concepto, self).save(*args, **kwargs)

	def edit_url(self):
		return "/manager/concepto/%s/editar" % self.slug

class Material(models.Model):
	concepto   = models.ForeignKey(Concepto)
	nombre     = models.CharField(max_length=50)
	slug       = models.SlugField()	
	#video     = models.CharField(max_length=200, blank=True, default="", help_text='La url donde se encuentra el video para el streaming')
	video      = models.FileField(upload_to="instructivos-videos/", blank=True)
	contenido  = FroalaField(null=True, blank=True)
	activo     = models.BooleanField(default=False)
	created_at = models.DateTimeField(auto_now_add=True)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name_plural = "Materiales"


	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.nombre)
		super(Material, self).save(*args, **kwargs)

	def edit_url(self):
		return "/manager/material/%s/editar/" % self.slug

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