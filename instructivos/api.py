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

#Import models
from .models import Concepto, Material, Pregunta, Examen, Orden
from usuarios.models import UserProfile, ExamenAprobado

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
        """
        API Login
        @params    cedula(Int) isAdmin (1 || 2)
        @response  id(int) nombre(String)
        """
        isAdmin = request.GET.get('isAdmin')
        cedula  = request.GET.get('cedula')

        # Si la cedula esta vacia
        if cedula is None or cedula == "":
            return APIResponse("", "Cedula vacia", 1)

        usuario = User.objects.get(username=cedula)

        # Para retornar si es admin o no
        if isAdmin == "1":
            isAdmin = True
        else:
            isAdmin = False

        if isAdmin:
            userInfo = UserProfile.objects.get(usuario=usuario)

            if userInfo.isAdmin:
                data = [{
                    "id": usuario.username,
                    "nombre": usuario.first_name + " " + usuario.last_name
                }]
                return APIResponse(data, "Usuario Administrador", 1)
            else:
                return APIResponse("", "Usuario no es administrador", 0)
        else:
            data = [{
                "id": usuario.username,
                "nombre": usuario.first_name + " " + usuario.last_name
            }]
            return APIResponse(data, "Trabajador", 1)
