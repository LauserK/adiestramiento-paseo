from django.conf.urls import url, include
from django.views.decorators.csrf import csrf_exempt

from instructivos.api import LoginApi

urls = [
	url(r'^login/$', csrf_exempt(LoginApi.as_view())),
]
