# -*- coding: utf-8 -*-
from django.shortcuts import render, redirect
from django.views.generic import View, TemplateView
from django.contrib.auth import authenticate, login, logout

class LoginView(TemplateView):
	def get(self, request):
		template_name = "login.html"
		return render(request, template_name)

	def post(self, request):
		template_name = "login.html"
		mensaje       = ""

		usuario       = request.POST.get("usuario")
		contrasena    = request.POST.get("clave")

		if usuario is not None and contrasena is not None and usuario != "" and contrasena != "":
			user = authenticate(username=usuario, password=contrasena)
			if user is not None:
				login(request, user)
				return redirect('/')
			else:
				mensaje = "¡Usuario/Contraseña Incorrecta!"

		else:
			mensaje = "No se deben dejar campos vacios"

		ctx = {
			"mensaje": mensaje
		}
		return render(request, template_name, ctx)



class LogoutView(View):
	def get(self, request):
		logout(request)
		return redirect('/')
