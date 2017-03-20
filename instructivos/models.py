from __future__ import unicode_literals
from django.db import models
from django.db.models.signals import post_save, post_delete
from django.dispatch.dispatcher import receiver
from django.template.defaultfilters import slugify
from froala_editor.fields import FroalaField
from django.conf import settings

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
	#video     = models.CharField(max_length=200, blank=True, default="", help_text='La url donde se encuentra el video para el streaming')
	video     = models.FileField(upload_to="instructivos-videos/", blank=True)
	contenido = FroalaField(null=True, blank=True)
	activo = models.BooleanField(default=False)

	def __unicode__(self):
		return self.nombre

	class Meta:
		verbose_name_plural = "Materiales"


	def save(self, *args, **kwargs):
		if not self.id:
			self.slug = slugify(self.nombre)
		super(Material, self).save(*args, **kwargs)

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


@receiver(post_save, sender=Concepto)
def rename_image(sender, instance, **kwargs):
	created = False
	if 'created' in kwargs:
		if kwargs['created']:
			created = True

	if instance.imagen and not created:
		ext = instance.imagen.name.split('.')[-1]
		filename = 'conceptos/{}.{}'.format(instance.pk, ext)
		direccion = instance.imagen.path
		dir_file = os.path.join(settings.MEDIA_ROOT, filename)
		if str(direccion) != str(dir_file):
			if os.path.exists(dir_file):
				os.remove(dir_file)
			os.rename(direccion, dir_file)
			Concepto.objects.filter(pk=instance.pk).update(imagen=filename)