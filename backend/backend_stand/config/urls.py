from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from stand.models import Veiculo


admin.site.site_header = "Administração Autogémeos"
admin.site.site_title = "Autogémeos Admin"
admin.site.index_title = "Painel de Gestão"


def home(request):
    veiculos = Veiculo.objects.filter(vei_estado="Disponível").order_by("-vei_criado_em")[:3]
    return render(request, "index.html", {"carros": veiculos})


def veiculos(request):
    return render(request, "veiculos.html")


def sobre(request):
    return render(request, "SobreNos.html")


def contacto(request):
    return render(request, "contacto.html")


def detalhe_veiculo(request, carro_id):
    carro = Veiculo.objects.filter(vei_id=carro_id).first()

    imagens = []
    if carro:
        imagens = carro.imagemveiculo_set.all().order_by("-img_capa", "img_id")

    return render(request, "detalhe_veiculo.html", {
        "carro": carro,
        "imagens": imagens,
    })


urlpatterns = [
    path("", home, name="home"),
    path("veiculos/", veiculos, name="veiculos"),
    path("sobre/", sobre, name="sobre"),
    path("contacto/", contacto, name="contacto"),
    path("veiculo/<int:carro_id>/", detalhe_veiculo, name="detalhe_veiculo"),

    path("admin/", admin.site.urls),
    path("api/", include("stand.urls")),
]