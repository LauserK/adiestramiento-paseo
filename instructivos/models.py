# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.db import models
from django.db.models.signals import post_save, post_delete, pre_delete
from django.dispatch.dispatcher import receiver
from django.template.defaultfilters import slugify
from froala_editor.fields import FroalaField
import datetime

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

	def delete_url(self):
		return "/manager/material/%s/eliminar/" % self.slug

	def get_video(self):
		return self.video.url

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
	ilustracion = models.ImageField(upload_to="examenes/", blank=True, default="")

	def __unicode__(self):
		return self.pregunta

	def get_image(self):
		return self.ilustracion.url

class Examen(models.Model):
	preguntas = models.ManyToManyField(Pregunta, blank=True)
	material  = models.OneToOneField(Material, blank=True, null=True)
	activo = models.BooleanField(default=False)

	def __unicode__(self):
		return "Examen %s" % self.material.nombre

	class Meta:
		verbose_name_plural = "Examenes"

	def view_url(self):
		return "/manager/examen/%s/" % self.pk

	def edit_url(self):
		return "/manager/examen/%s/editar/" % self.pk

	def delete_url(self):
		return "/manager/examen/%s/eliminar/" % self.pk

	def add_answer(self):
		return "/manager/examen/%s/pregunta/" % self.pk

class Orden(models.Model):
	instructivo_1  = models.ForeignKey(Material, related_name='intructivo_1',  blank=True, null=True)
	instructivo_2  = models.ForeignKey(Material, related_name='intructivo_2',  blank=True, null=True)
	instructivo_3  = models.ForeignKey(Material, related_name='intructivo_3',  blank=True, null=True)
	instructivo_4  = models.ForeignKey(Material, related_name='intructivo_4',  blank=True, null=True)
	instructivo_5  = models.ForeignKey(Material, related_name='intructivo_5',  blank=True, null=True)
	instructivo_6  = models.ForeignKey(Material, related_name='intructivo_6',  blank=True, null=True)
	instructivo_7  = models.ForeignKey(Material, related_name='intructivo_7',  blank=True, null=True)
	instructivo_8  = models.ForeignKey(Material, related_name='intructivo_8',  blank=True, null=True)
	instructivo_9  = models.ForeignKey(Material, related_name='intructivo_9',  blank=True, null=True)
	instructivo_10 = models.ForeignKey(Material, related_name='intructivo_10', blank=True, null=True)
	instructivo_11 = models.ForeignKey(Material, related_name='intructivo_11', blank=True, null=True)
	instructivo_12 = models.ForeignKey(Material, related_name='intructivo_12', blank=True, null=True)
	instructivo_13 = models.ForeignKey(Material, related_name='intructivo_13', blank=True, null=True)
	instructivo_14 = models.ForeignKey(Material, related_name='intructivo_14', blank=True, null=True)
	instructivo_15 = models.ForeignKey(Material, related_name='intructivo_15', blank=True, null=True)
	instructivo_16 = models.ForeignKey(Material, related_name='intructivo_16', blank=True, null=True)
	instructivo_17 = models.ForeignKey(Material, related_name='intructivo_17', blank=True, null=True)
	instructivo_18 = models.ForeignKey(Material, related_name='intructivo_18', blank=True, null=True)
	instructivo_19 = models.ForeignKey(Material, related_name='intructivo_19', blank=True, null=True)
	instructivo_20 = models.ForeignKey(Material, related_name='intructivo_20', blank=True, null=True)
	instructivo_21 = models.ForeignKey(Material, related_name='intructivo_21', blank=True, null=True)
	instructivo_22 = models.ForeignKey(Material, related_name='intructivo_22', blank=True, null=True)
	instructivo_23 = models.ForeignKey(Material, related_name='intructivo_23', blank=True, null=True)
	instructivo_24 = models.ForeignKey(Material, related_name='intructivo_24', blank=True, null=True)
	instructivo_25 = models.ForeignKey(Material, related_name='intructivo_25', blank=True, null=True)
	instructivo_26 = models.ForeignKey(Material, related_name='intructivo_26', blank=True, null=True)
	instructivo_27 = models.ForeignKey(Material, related_name='intructivo_27', blank=True, null=True)
	instructivo_28 = models.ForeignKey(Material, related_name='intructivo_28', blank=True, null=True)
	instructivo_29 = models.ForeignKey(Material, related_name='intructivo_29', blank=True, null=True)
	instructivo_30 = models.ForeignKey(Material, related_name='intructivo_30', blank=True, null=True)


	class Meta:
		verbose_name_plural = "Orden de visualización de instructivos"

	def __unicode__(self):
		return "PULSE AQUÍ"

@receiver(pre_delete, sender=Material)
def Material_delete(sender, instance, **kwargs):
	instance.video.delete()
