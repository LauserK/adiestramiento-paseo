from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
from instructivos.models import Material, Concepto, Examen
from django.core.validators import MaxValueValidator, MinValueValidator

class UserProfile(models.Model):
    usuario              = models.OneToOneField(User)
    isAdmin              = models.BooleanField(default=False)
    materiales_aprobados = models.ManyToManyField(Material, blank=True)
    cedula               = models.CharField(max_length=10, default="", blank=True)

    class Meta:
    	verbose_name='Perfil de usuario'

    def __unicode__(self):
        return self.usuario.username

    def get_avatar(self):
        return '%s%s' % (settings.MEDIA_URL,self.avatar)

    def create_profile(sender, instance, created, **kwargs):
        if created:
            UserProfile.objects.create(usuario=instance)
    post_save.connect(create_profile, sender=User)

class ExamenAprobado(models.Model):
    usuario  = models.ForeignKey(User)
    examen   = models.ForeignKey(Examen)
    nota     = models.IntegerField(default=0, validators=[MaxValueValidator(20), MinValueValidator(0)])
    aprobado = models.BooleanField(default=False)

    class Meta:
        verbose_name='Examenes realizados'

    def get_aprobado(self):
        if self.aprobado == True:
            return "Aprobado"
        else:
            return "Reprobado"

    def __unicode__(self):
        return "%s - %s - %s" % (self.aprobado, self.usuario.username, self.examen.material.nombre)
