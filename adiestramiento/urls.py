"""adiestramiento URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from instructivos.views import CourseView, AddConceptView, AddMaterialView, RemoveConceptView, EditConceptView, EditMaterialView, RemoveMaterialView
from usuarios.views import LoginView, LogoutView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', CourseView.as_view()),
    url(r'^login/$', LoginView.as_view() ),
    url(r'^manager/concepto/agregar/$', AddConceptView.as_view(), name="add-concept" ),
    url(r'^manager/concepto/(?P<conceptSlug>[-\w]+)/agregar-material/$', AddMaterialView.as_view(), name="add-material"),
    url(r'^manager/concepto/(?P<conceptSlug>[-\w]+)/eliminar/$', RemoveConceptView.as_view(), name="remove-concept"),
    url(r'^manager/concepto/(?P<conceptSlug>[-\w]+)/editar/$', EditConceptView.as_view(), name="edit-concept"),
    url(r'^manager/material/(?P<materialSlug>[-\w]+)/editar/$', EditMaterialView.as_view(), name="edit-material"),
    url(r'^manager/material/(?P<materialSlug>[-\w]+)/eliminar/$', RemoveMaterialView.as_view(), name="remove-material"),
    url(r'^logout/$', LogoutView.as_view() ),
]
"""
+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
"""
