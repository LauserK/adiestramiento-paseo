from django.conf.urls import url, include
from django.contrib import admin
from instructivos.views import CourseView, AddConceptView, AddMaterialView, RemoveConceptView, EditConceptView, EditMaterialView, RemoveMaterialView, ExamenView, AddExamenView, EditExamenView, RemoveExamenView, SingleExamenView, AddPregunta, EditPregunta, RemovePregunta
from usuarios.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static
from django.views.generic.base import RedirectView

#Import API URLS
from instructivos import api_urls

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', CourseView.as_view()),
    url(r'^api/', include(api_urls.urls)),
    url(r'^login/$', LoginView.as_view() ),
    url(r'^order/$', RedirectView.as_view(url='/admin/instructivos/orden/1/change/', permanent=False),name="order"),
    # URL CONCEPTO
    url(r'^manager/concepto/agregar/$', AddConceptView.as_view(), name="add-concept" ),
    url(r'^manager/concepto/(?P<conceptSlug>[-\w]+)/agregar-material/$', AddMaterialView.as_view(), name="add-material"),
    url(r'^manager/concepto/(?P<conceptSlug>[-\w]+)/eliminar/$', RemoveConceptView.as_view(), name="remove-concept"),
    url(r'^manager/concepto/(?P<conceptSlug>[-\w]+)/editar/$', EditConceptView.as_view(), name="edit-concept"),
    # URL MATERIAL
    url(r'^manager/material/(?P<materialSlug>[-\w]+)/editar/$', EditMaterialView.as_view(), name="edit-material"),
    url(r'^manager/material/(?P<materialSlug>[-\w]+)/eliminar/$', RemoveMaterialView.as_view(), name="remove-material"),
    # URL EXAMEN
    url(r'^manager/examen/$', ExamenView.as_view(), name="show-examenes"),
    url(r'^manager/examen/agregar/$', AddExamenView.as_view(), name="add-examenes"),
    url(r'^manager/examen/(?P<examenSlug>[-\w]+)/$', SingleExamenView.as_view(), name="single-examenes"),
    url(r'^manager/examen/(?P<examenSlug>[-\w]+)/pregunta/(?P<preguntaId>[-\w]+)/eliminar/$', RemovePregunta.as_view(), name="remove-pregunta"),
    url(r'^manager/examen/(?P<examenSlug>[-\w]+)/pregunta/(?P<preguntaId>[-\w]+)$', EditPregunta.as_view(), name="edit-pregunta"),
    url(r'^manager/examen/(?P<examenSlug>[-\w]+)/pregunta/$', AddPregunta.as_view(), name="add-pregunta"),
    url(r'^manager/examen/(?P<examenSlug>[-\w]+)/editar/$', EditExamenView.as_view(), name="edit-examenes"),
    url(r'^manager/examen/(?P<examenSlug>[-\w]+)/eliminar/$', RemoveExamenView.as_view(), name="remove-examenes"),
    url(r'^logout/$', LogoutView.as_view() ),
]
"""
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
