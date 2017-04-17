from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt
from instructivo.api import LoginApi

#Import VIEWS

urls = [
	url(r'^login/$', csrf_exempt(LoginApi.as_view())),
]
