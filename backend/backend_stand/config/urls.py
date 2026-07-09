from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render


def home(request):
    return render(request, "index.html")


def veiculos(request):
    return render(request, "veiculos.html")


def sobre(request):
    return render(request, "SobreNos.html")


def contacto(request):
    return render(request, "contacto.html")


urlpatterns = [
    path("", home, name="home"),
    path("veiculos/", veiculos, name="veiculos"),
    path("sobre/", sobre, name="sobre"),
    path("contacto/", contacto, name="contacto"),

    path("admin/", admin.site.urls),
    path("api/", include("stand.urls")),
]