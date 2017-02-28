from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.conf import settings
"""
class UserProfile(models.Model):  
    usuario = models.OneToOneField(User)        
    cursos = models.ManyToManyField(Curso, blank=True)
    suscripciones = (
    	('gratuita', 'Gratuita'),
    	('mensual', 'Mensual'),
    	('anual', 'Anual'),
    )
    suscripcion = models.CharField(max_length=10, choices=suscripciones, default='gratuita')
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
"""