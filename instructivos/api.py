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

        try:
            usuario = User.objects.get(username=cedula)
        except ObjectDoesNotExist:
            return APIResponse("", "Usuario inexistente", 0)

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

class RegisterApi(View):
    def get(self, request):
        """
        API Register
        @params    cedula(Int)
        @response  cedula(int) nombre(String) apellido(String) nombre_completo(String)
        """
        cedula = request.GET.get('cedula')

        if cedula is None or cedula == "":
            return APIResponse("", "Cedula vacia", 0)

        userInfo = UserProfile.objects.filter(cedula=cedula)
        if userInfo.exists():
            userInfo = UserProfile.objects.get(cedula=cedula)
            data = {
                "nombre": userInfo.usuario.first_name,
                "apellido": userInfo.usuario.last_name,
                "cedula": userInfo.cedula
            }
            return APIResponse(data, "Usuario existente", 0)

        cursor = connections['RUU'].cursor()
        cursor.execute("SELECT nombres, apellidos, cedula FROM `nomina` WHERE `cedula` LIKE '%"+cedula+"'")
        row = cursor.fetchone()#fetchall()

        if row is None:
            return APIResponse("", "Cedula inexistente en RUU", 0)

        nombre    = row[0]
        apellido  = row[1]
        cedula    = cedula

        # Crear usuario
        new_user            = User.objects.create_user(cedula, 'it@grupopaseo.com', 'Paseo2017')
        new_user.first_name = nombre
        new_user.last_name  = apellido
        new_user.save()
        userInfo            = UserProfile.objects.get(usuario=new_user)
        userInfo.cedula     = cedula
        userInfo.save()

        data = {
            "nombre": nombre,
            "apellido": apellido,
            "cedula": cedula,
            "nombre_completo": "%s %s" % (nombre, apellido)
        }
        return APIResponse(data, "Trabajador creado", 1)

class GetNextInstructivo(View):
    def get(self, request):
        """
        API GetNextInstructivo
        @params    cedula(Int)
        @response  nombre(String) urlVideo(String) contenido(String)
        """

        cedula = request.GET.get('cedula')

        if cedula is None or cedula == "":
            return APIResponse("", "Cedula vacia", 0)

        userInfo = UserProfile.objects.filter(cedula=cedula)
        if not userInfo.exists():
            return APIResponse("", "Usuario inexistente", 0)
        else:
            userInfo = UserProfile.objects.get(cedula=cedula)


        orden_visualizacion = Orden.objects.all().first()
        #total_instructivos  = len(orden_visualizacion._meta.get_fields()) - 1
        counter = 1
        instructivo = None
        for i in orden_visualizacion._meta.get_fields():
            if counter == 1:
                instructivo = orden_visualizacion.instructivo_1
            elif counter == 2:
                instructivo = orden_visualizacion.instructivo_2
            elif counter == 3:
                instructivo = orden_visualizacion.instructivo_3
            elif counter == 4:
                instructivo = orden_visualizacion.instructivo_4
            elif counter == 5:
                instructivo = orden_visualizacion.instructivo_5
            elif counter == 6:
                instructivo = orden_visualizacion.instructivo_6
            elif counter == 7:
                instructivo = orden_visualizacion.instructivo_7
            elif counter == 8:
                instructivo = orden_visualizacion.instructivo_8
            elif counter == 9:
                instructivo = orden_visualizacion.instructivo_9
            elif counter == 10:
                instructivo = orden_visualizacion.instructivo_10

            if instructivo not in userInfo.materiales_aprobados.all():
                if instructivo is not None:
                    if instructivo.activo == True:
                        break
                    else:
                        instructivo == None

            counter += 1

        if instructivo is None:
            return APIResponse("", "No hay instructivos pendientes", 1)

        data = {
            "id": instructivo.pk,
            "nombre": instructivo.nombre,
            "urlVideo": instructivo.get_video(),
            "contenido": instructivo.contenido
        }

        return APIResponse(data, "Instructivo obtenido!", 1)

class GetExamen(View):
    def get(self, request):
        instructivo_id = request.GET.get('instructivo_id')
        cedula         = request.GET.get('cedula')

        if instructivo_id is None or instructivo_id == "":
            return APIResponse("", "instructivo_id esta vacio", 0)

        if cedula is None or cedula == "":
            return APIResponse("", "cedula esta vacia", 0)

        userInfo = UserProfile.objects.filter(cedula=cedula)
        if not userInfo.exists():
            return APIResponse("", "Usuario inexistente", 0)
        else:
            userInfo = UserProfile.objects.get(cedula=cedula)

        try:
            examen = Examen.objects.get(material__pk=instructivo_id)
        except ObjectDoesNotExist:
            return APIResponse("", "Examen inexistente!", 0)

        material = Material.objects.get(pk=instructivo_id)
        if material in userInfo.materiales_aprobados.all():
            return APIResponse("", "Examen ya aprobado por el usuario!", 0)

        preguntas = list(examen.preguntas.all().values())
        d = 0
        for i in preguntas:
            del preguntas[d]['opcion_correcta']
            d += 1

        data = {
            "nombre": examen.material.nombre,
            "preguntas": preguntas
        }

        return APIResponse(data, "", 1)

class PostExamen(View):
    def get(self, request):
        instructivo_id = request.GET.get('instructivo_id')
        pregunta_1     = request.GET.get('res1')
        pregunta_2     = request.GET.get('res2')
        pregunta_3     = request.GET.get('res3')
        pregunta_4     = request.GET.get('res4')
        pregunta_5     = request.GET.get('res5')
        pregunta_6     = request.GET.get('res6')
        pregunta_7     = request.GET.get('res7')
        pregunta_8     = request.GET.get('res8')
        pregunta_9     = request.GET.get('res9')
        pregunta_10    = request.GET.get('res10')
        pregunta_11    = request.GET.get('res11')
        pregunta_12    = request.GET.get('res12')
        pregunta_13    = request.GET.get('res13')
        pregunta_14    = request.GET.get('res14')
        pregunta_15    = request.GET.get('res15')
        pregunta_16    = request.GET.get('res16')
        pregunta_17    = request.GET.get('res17')
        pregunta_18    = request.GET.get('res18')
        pregunta_19    = request.GET.get('res19')
        pregunta_20    = request.GET.get('res20')
        pregunta_20    = request.GET.get('res21')
        pregunta_20    = request.GET.get('res22')
        pregunta_20    = request.GET.get('res23')
        pregunta_20    = request.GET.get('res24')
        pregunta_20    = request.GET.get('res25')
        pregunta_20    = request.GET.get('res26')
        pregunta_20    = request.GET.get('res27')
        pregunta_20    = request.GET.get('res28')
        pregunta_20    = request.GET.get('res29')
        pregunta_20    = request.GET.get('res30')

        try:
            examen     = Examen.objects.get(material__pk=instructivo_id)
        except ObjectDoesNotExist:
            return APIResponse("", "Examen inexistente", 0)

        if pregunta_1 is None or pregunta_2 is None or pregunta_3 is None or pregunta_4 is None or pregunta_5 is None or pregunta_6 is None or pregunta_7 is None or pregunta_8 is None or pregunta_9 is None or pregunta_10 is None:
            return APIResponse("", "Alguna respuesta esta vacia", 0)
        elif pregunta_11 is None or pregunta_12 is None or pregunta_13 is None or pregunta_14 is None or pregunta_15 is None or pregunta_16 is None or pregunta_17 is None or pregunta_18 is None or pregunta_19 is None or pregunta_20 is None:
            return APIResponse("", "Alguna respuesta esta vacia", 0)

        respuestas = []

        for i in range(1,21):
            respuestas.append(request.GET.get('res%i' % i))

        print respuestas

        return APIResponse("", "", 1)
