from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt

from instructivos.api import LoginApi, RegisterApi, GetNextInstructivo, GetExamen, PostExamen

urls = [
	url(r'^login/$', csrf_exempt(LoginApi.as_view())),
	url(r'^register/$', csrf_exempt(RegisterApi.as_view())),
	url(r'^instructivo/$', csrf_exempt(GetNextInstructivo.as_view())),
	url(r'^examen/$', csrf_exempt(GetExamen.as_view())),
]
