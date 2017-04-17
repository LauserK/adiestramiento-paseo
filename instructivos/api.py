# -*- coding: utf-8 -*-
from django.conf import settings
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.generic import View
from django.db import connection, connections
import datetime, json, os

def APIResponse(data, message, success):
    """
    Utilidad para responder la peticion con una respuesta en json
    """
	settings = {
		"success": success,
		"message": message
	}
	if data is not None:
		return JsonResponse({"data": data, "settings":settings})
	else:
		return JsonResponse({"data": [], "settings": settings})

class LoginApi(View):
    def get(self, request):
        return APIResponse("", "HOLA", 1)
