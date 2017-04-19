from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt

from instructivos.api import LoginApi, RegisterApi

urls = [
	url(r'^login/$', csrf_exempt(LoginApi.as_view())),
	url(r'^register/$', csrf_exempt(RegisterApi.as_view())),
]
