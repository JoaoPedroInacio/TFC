from django.contrib import admin
from django.core.mail import send_mail
from django.conf import settings
from .google_calendar import criar_evento_test_drive
from .models import (
    Combustivel,
    Marca,
    Modelo,
    Veiculo,
    ImagemVeiculo,
    FinanciamentoVeiculo,
    SimulacaoCredito,
    TestDrive,
    Utilizador,
)


class ImagemVeiculoInline(admin.TabularInline):
    model = ImagemVeiculo
    extra = 1


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = (
        "vei_id",
        "vei_mdl",
        "vei_matricula",
        "vei_ano",
        "vei_quilometros",
        "vei_preco_venda",
        "vei_estado",
        "vei_destaque",
    )

    list_filter = (
        "vei_estado",
        "vei_cmb",
        "vei_ano",
        "vei_mdl__mdl_mrc",
        "vei_destaque",
    )

    search_fields = (
        "vei_matricula",
        "vei_vin",
        "vei_mdl__mdl_nome",
        "vei_mdl__mdl_mrc__mrc_nome",
    )

    list_editable = (
        "vei_destaque",
    )

    inlines = [ImagemVeiculoInline]


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ("mrc_id", "mrc_nome")
    search_fields = ("mrc_nome",)


@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ("mdl_id", "mdl_mrc", "mdl_nome")
    list_filter = ("mdl_mrc",)
    search_fields = ("mdl_nome", "mdl_mrc__mrc_nome")


@admin.register(Combustivel)
class CombustivelAdmin(admin.ModelAdmin):
    list_display = ("cmb_id", "cmb_nome")
    search_fields = ("cmb_nome",)


@admin.register(ImagemVeiculo)
class ImagemVeiculoAdmin(admin.ModelAdmin):
    list_display = ("img_id", "img_vei", "img_capa", "img_caminho")
    list_filter = ("img_capa",)
    search_fields = (
        "img_vei__vei_matricula",
        "img_vei__vei_mdl__mdl_nome",
        "img_caminho",
    )


@admin.register(FinanciamentoVeiculo)
class FinanciamentoVeiculoAdmin(admin.ModelAdmin):
    list_display = ("fin_id", "fin_vei", "fin_prazo_meses", "fin_prestacao")
    search_fields = ("fin_vei__vei_matricula", "fin_vei__vei_mdl__mdl_nome")


@admin.register(SimulacaoCredito)
class SimulacaoCreditoAdmin(admin.ModelAdmin):
    list_display = ("sim_id", "sim_usr", "sim_vei", "sim_prazo_meses", "sim_prestacao")
    search_fields = ("sim_usr__usr_nome", "sim_vei__vei_matricula")


@admin.register(TestDrive)
class TestDriveAdmin(admin.ModelAdmin):
    list_display = (
        "tdr_id",
        "tdr_nome",
        "tdr_email",
        "tdr_telefone",
        "tdr_vei",
        "tdr_data",
        "tdr_hora",
        "tdr_estado",
        "tdr_criado_em",
    )

    list_filter = (
        "tdr_estado",
        "tdr_data",
        "tdr_hora",
    )

    search_fields = (
        "tdr_nome",
        "tdr_email",
        "tdr_telefone",
        "tdr_vei__vei_matricula",
        "tdr_vei__vei_mdl__mdl_nome",
        "tdr_vei__vei_mdl__mdl_mrc__mrc_nome",
    )

    list_editable = (
        "tdr_estado",
    )

    readonly_fields = (
        "tdr_criado_em",
    )

    ordering = (
        "-tdr_data",
        "-tdr_hora",
    )

    def save_model(self, request, obj, form, change):
        estado_antigo = None

        if change:
            try:
                estado_antigo = TestDrive.objects.get(pk=obj.pk).tdr_estado
            except TestDrive.DoesNotExist:
                estado_antigo = None

        super().save_model(request, obj, form, change)

        if estado_antigo != obj.tdr_estado:
            try:
                criar_evento_test_drive(obj)
            except Exception as e:
                print(f"Erro ao criar evento no Google Calendar: {e}")

            if obj.tdr_estado == TestDrive.ESTADO_CONFIRMADO:
                assunto = "Test-drive confirmado - Autogémeos"

                mensagem = f"""
Olá {obj.tdr_nome},

O seu test-drive foi confirmado pela equipa Autogémeos.

Veículo: {obj.tdr_vei.marca} {obj.tdr_vei.modelo}
Data: {obj.tdr_data.strftime('%d/%m/%Y')}
Hora: {obj.tdr_hora.strftime('%H:%M')}

Aguardamos por si na data e hora marcada.

Obrigado,
Autogémeos
"""

                send_mail(
                    assunto,
                    mensagem,
                    getattr(settings, "DEFAULT_FROM_EMAIL", "tfcautogemeos@gmail.com"),
                    [obj.tdr_email],
                    fail_silently=False,
                )

            elif obj.tdr_estado == TestDrive.ESTADO_CANCELADO:
                assunto = "Test-drive cancelado - Autogémeos"

                mensagem = f"""
Olá {obj.tdr_nome},

Informamos que o seu test-drive foi cancelado pela equipa Autogémeos.

Veículo: {obj.tdr_vei.marca} {obj.tdr_vei.modelo}
Data: {obj.tdr_data.strftime('%d/%m/%Y')}
Hora: {obj.tdr_hora.strftime('%H:%M')}

Para remarcar, por favor contacte-nos ou faça um novo pedido no website.

Obrigado,
Autogémeos
"""

                send_mail(
                    assunto,
                    mensagem,
                    getattr(settings, "DEFAULT_FROM_EMAIL", "tfcautogemeos@gmail.com"),
                    [obj.tdr_email],
                    fail_silently=False,
                )
            
@admin.register(Utilizador)
class UtilizadorAdmin(admin.ModelAdmin):
    list_display = ("usr_id", "usr_nome", "usr_email", "usr_telefone", "usr_tipo")
    search_fields = ("usr_nome", "usr_email", "usr_telefone")
    list_filter = ("usr_tipo",)