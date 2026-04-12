import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError

from .models import Veiculo, Modelo, Combustivel


def veiculo_para_dict(veiculo):
    return {
        "vei_id": veiculo.vei_id,
        "marca": veiculo.vei_mdl.mdl_mrc.mrc_nome,
        "modelo": veiculo.vei_mdl.mdl_nome,
        "combustivel": veiculo.vei_cmb.cmb_nome if veiculo.vei_cmb else None,
        "vei_matricula": veiculo.vei_matricula,
        "vei_vin": veiculo.vei_vin,
        "vei_versao": veiculo.vei_versao,
        "vei_importado": veiculo.vei_importado,
        "vei_mes": veiculo.vei_mes,
        "vei_ano": veiculo.vei_ano,
        "vei_quilometros": veiculo.vei_quilometros,
        "vei_cilindrada": veiculo.vei_cilindrada,
        "vei_potencia_cv": veiculo.vei_potencia_cv,
        "vei_preco_venda": str(veiculo.vei_preco_venda),
        "vei_estado": veiculo.vei_estado,
        "vei_descricao": veiculo.vei_descricao,
        "vei_criado_em": veiculo.vei_criado_em,
        "vei_atualizado_em": veiculo.vei_atualizado_em,
    }


def listar_veiculos(request):
    if request.method != "GET":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    veiculos = Veiculo.objects.select_related("vei_mdl__mdl_mrc", "vei_cmb").all()
    data = [veiculo_para_dict(veiculo) for veiculo in veiculos]

    return JsonResponse(data, safe=False)


def detalhe_veiculo(request, id):
    if request.method != "GET":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    veiculo = get_object_or_404(
        Veiculo.objects.select_related("vei_mdl__mdl_mrc", "vei_cmb"),
        vei_id=id
    )

    return JsonResponse(veiculo_para_dict(veiculo))


@csrf_exempt
def criar_veiculo(request):
    if request.method != "POST":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    try:
        body = json.loads(request.body)

        modelo = get_object_or_404(Modelo, mdl_id=body.get("vei_mdl"))
        combustivel = None

        if body.get("vei_cmb"):
            combustivel = get_object_or_404(Combustivel, cmb_id=body.get("vei_cmb"))

        veiculo = Veiculo(
            vei_mdl=modelo,
            vei_cmb=combustivel,
            vei_matricula=body.get("vei_matricula"),
            vei_vin=body.get("vei_vin"),
            vei_versao=body.get("vei_versao"),
            vei_importado=body.get("vei_importado", False),
            vei_mes=body.get("vei_mes"),
            vei_ano=body.get("vei_ano"),
            vei_quilometros=body.get("vei_quilometros"),
            vei_cilindrada=body.get("vei_cilindrada"),
            vei_potencia_cv=body.get("vei_potencia_cv"),
            vei_preco_venda=body.get("vei_preco_venda"),
            vei_estado=body.get("vei_estado", "Disponível"),
            vei_descricao=body.get("vei_descricao"),
        )

        veiculo.full_clean()
        veiculo.save()

        return JsonResponse(veiculo_para_dict(veiculo), status=201)

    except ValidationError as e:
        return JsonResponse({"erros": e.message_dict}, status=400)

    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=400)

@csrf_exempt
def editar_veiculo(request, id):
    if request.method != "PUT":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    veiculo = get_object_or_404(Veiculo, vei_id=id)

    try:
        body = json.loads(request.body)

        if "vei_mdl" in body:
            veiculo.vei_mdl = get_object_or_404(Modelo, mdl_id=body["vei_mdl"])

        if "vei_cmb" in body:
            if body["vei_cmb"] is None:
                veiculo.vei_cmb = None
            else:
                veiculo.vei_cmb = get_object_or_404(Combustivel, cmb_id=body["vei_cmb"])

        veiculo.vei_matricula = body.get("vei_matricula", veiculo.vei_matricula)
        veiculo.vei_vin = body.get("vei_vin", veiculo.vei_vin)
        veiculo.vei_versao = body.get("vei_versao", veiculo.vei_versao)
        veiculo.vei_importado = body.get("vei_importado", veiculo.vei_importado)
        veiculo.vei_mes = body.get("vei_mes", veiculo.vei_mes)
        veiculo.vei_ano = body.get("vei_ano", veiculo.vei_ano)
        veiculo.vei_quilometros = body.get("vei_quilometros", veiculo.vei_quilometros)
        veiculo.vei_cilindrada = body.get("vei_cilindrada", veiculo.vei_cilindrada)
        veiculo.vei_potencia_cv = body.get("vei_potencia_cv", veiculo.vei_potencia_cv)
        veiculo.vei_preco_venda = body.get("vei_preco_venda", veiculo.vei_preco_venda)
        veiculo.vei_estado = body.get("vei_estado", veiculo.vei_estado)
        veiculo.vei_descricao = body.get("vei_descricao", veiculo.vei_descricao)

        veiculo.full_clean()
        veiculo.save()

        return JsonResponse(veiculo_para_dict(veiculo))

    except ValidationError as e:
        return JsonResponse({"erros": e.message_dict}, status=400)

    except Exception as e:
        return JsonResponse({"erro": str(e)}, status=400)

@csrf_exempt
def apagar_veiculo(request, id):
    if request.method != "DELETE":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    veiculo = get_object_or_404(Veiculo, vei_id=id)
    veiculo.delete()

    return JsonResponse({"mensagem": "Veículo apagado com sucesso"})