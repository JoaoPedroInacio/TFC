import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.exceptions import ValidationError
from django.db.models import Q, Min, Max

from .models import Veiculo, Modelo, Combustivel, Marca


def veiculo_para_dict(veiculo):
    return {
        "id": veiculo.id,
        "marca": veiculo.marca,
        "modelo": veiculo.modelo,
        "preco": veiculo.preco,
        "ano": veiculo.ano,
        "kms": veiculo.kms,
        "combustivel": veiculo.combustivel,
        "img": veiculo.img,

        "vei_id": veiculo.vei_id,
        "vei_matricula": veiculo.vei_matricula,
        "vei_vin": veiculo.vei_vin,
        "vei_versao": veiculo.vei_versao,
        "vei_importado": veiculo.vei_importado,
        "vei_mes": veiculo.vei_mes,
        "vei_cilindrada": veiculo.vei_cilindrada,
        "vei_potencia_cv": veiculo.vei_potencia_cv,
        "vei_estado": veiculo.vei_estado,
        "vei_descricao": veiculo.vei_descricao,
    }


def limpar_numero(valor):
    if not valor:
        return None

    try:
        valor_limpo = str(valor).replace(" ", "").replace(".", "").replace(",", "")
        return int(valor_limpo)
    except ValueError:
        return None


def criar_query_pesquisa_flexivel(pesquisa):
    """
    Pesquisa flexível para procurar por:
    - marca
    - modelo
    - versão
    - combustível
    - descrição
    - ano
    - potência
    - cilindrada

    Também trata casos como:
    - serie / série
    - classe a
    - golf gti
    - dsg
    """

    pesquisa = pesquisa.strip()

    if not pesquisa:
        return Q()

    termos_extra = []

    pesquisa_lower = pesquisa.lower()

    aliases = {
        "serie": ["serie", "série"],
        "série": ["serie", "série"],
        "classe a": ["classe a", "a 180", "a180", "a 200", "a200"],
        "golf": ["golf", "gti", "gtd", "r"],
        "gti": ["gti"],
        "dsg": ["dsg"],
    }

    termos_extra.append(pesquisa)

    for chave, valores in aliases.items():
        if chave in pesquisa_lower:
            termos_extra.extend(valores)

    # Divide também a pesquisa por palavras.
    # Exemplo: "golf gti" procura por "golf", "gti" e pela frase completa.
    palavras = pesquisa.split()
    for palavra in palavras:
        if len(palavra) >= 2:
            termos_extra.append(palavra)

    query = Q()

    for termo in set(termos_extra):
        query |= Q(vei_mdl__mdl_nome__icontains=termo)
        query |= Q(vei_mdl__mdl_mrc__mrc_nome__icontains=termo)
        query |= Q(vei_cmb__cmb_nome__icontains=termo)
        query |= Q(vei_versao__icontains=termo)
        query |= Q(vei_descricao__icontains=termo)
        query |= Q(vei_ano__icontains=termo)
        query |= Q(vei_potencia_cv__icontains=termo)
        query |= Q(vei_cilindrada__icontains=termo)

    return query

def listar_veiculos(request):
    if request.method != "GET":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    veiculos = Veiculo.objects.select_related(
        "vei_mdl__mdl_mrc",
        "vei_cmb"
    ).filter(vei_estado="Disponível")

    pesquisa = request.GET.get("pesquisa", "").strip()
    q = request.GET.get("q", "").strip()

    # Aceita tanto ?pesquisa=golf como ?q=golf
    termo_pesquisa = pesquisa or q

    marca = request.GET.get("marca", "").strip()
    combustiveis = request.GET.getlist("combustivel")

    preco_min = limpar_numero(request.GET.get("preco_min"))
    preco_max = limpar_numero(request.GET.get("preco_max"))

    ano_min = limpar_numero(request.GET.get("ano_min"))
    ano_max = limpar_numero(request.GET.get("ano_max"))

    kms_min = limpar_numero(request.GET.get("kms_min"))
    kms_max = limpar_numero(request.GET.get("kms_max"))

    if termo_pesquisa:
        veiculos = veiculos.filter(criar_query_pesquisa_flexivel(termo_pesquisa))

    if marca and marca != "Todas as Marcas":
        veiculos = veiculos.filter(vei_mdl__mdl_mrc__mrc_nome__iexact=marca)

    if combustiveis:
        veiculos = veiculos.filter(vei_cmb__cmb_nome__in=combustiveis)

    if preco_min is not None:
        veiculos = veiculos.filter(vei_preco_venda__gte=preco_min)

    if preco_max is not None:
        veiculos = veiculos.filter(vei_preco_venda__lte=preco_max)

    if ano_min is not None:
        veiculos = veiculos.filter(vei_ano__gte=ano_min)

    if ano_max is not None:
        veiculos = veiculos.filter(vei_ano__lte=ano_max)

    if kms_min is not None:
        veiculos = veiculos.filter(vei_quilometros__gte=kms_min)

    if kms_max is not None:
        veiculos = veiculos.filter(vei_quilometros__lte=kms_max)

    veiculos = veiculos.distinct().order_by("-vei_criado_em")

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


def filtros_veiculos(request):
    if request.method != "GET":
        return JsonResponse({"erro": "Método não permitido"}, status=405)

    marcas = Marca.objects.order_by("mrc_nome").values_list("mrc_nome", flat=True)
    combustiveis = Combustivel.objects.order_by("cmb_nome").values_list("cmb_nome", flat=True)

    limites = Veiculo.objects.filter(
        vei_estado="Disponível"
    ).aggregate(
        preco_min=Min("vei_preco_venda"),
        preco_max=Max("vei_preco_venda"),
        ano_min=Min("vei_ano"),
        ano_max=Max("vei_ano"),
        kms_min=Min("vei_quilometros"),
        kms_max=Max("vei_quilometros"),
    )

    return JsonResponse({
        "marcas": list(marcas),
        "combustiveis": list(combustiveis),
        "limites": limites,
    })