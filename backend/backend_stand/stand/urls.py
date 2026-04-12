from django.urls import path
from .views import (
    listar_veiculos,
    detalhe_veiculo,
    criar_veiculo,
    editar_veiculo,
    apagar_veiculo,
)

urlpatterns = [
    path("veiculos/", listar_veiculos, name="listar_veiculos"),
    path("veiculos/<int:id>/", detalhe_veiculo, name="detalhe_veiculo"),
    path("veiculos/criar/", criar_veiculo, name="criar_veiculo"),
    path("veiculos/<int:id>/editar/", editar_veiculo, name="editar_veiculo"),
    path("veiculos/<int:id>/apagar/", apagar_veiculo, name="apagar_veiculo"),
]