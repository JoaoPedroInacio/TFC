from django.contrib import admin
from .models import (
    Combustivel,
    Marca,
    Modelo,
    Utilizador,
    Veiculo,
    ImagemVeiculo,
    FinanciamentoVeiculo,
    SimulacaoCredito,
    TestDrive,
)


@admin.register(Marca)
class MarcaAdmin(admin.ModelAdmin):
    list_display = ('mrc_id', 'mrc_nome')
    search_fields = ('mrc_nome',)


@admin.register(Modelo)
class ModeloAdmin(admin.ModelAdmin):
    list_display = ('mdl_id', 'mdl_nome', 'mdl_mrc')
    list_filter = ('mdl_mrc',)
    search_fields = ('mdl_nome', 'mdl_mrc__mrc_nome')


@admin.register(Combustivel)
class CombustivelAdmin(admin.ModelAdmin):
    list_display = ('cmb_id', 'cmb_nome')
    search_fields = ('cmb_nome',)


@admin.register(Veiculo)
class VeiculoAdmin(admin.ModelAdmin):
    list_display = (
        'vei_id',
        'vei_mdl',
        'vei_cmb',
        'vei_matricula',
        'vei_ano',
        'vei_quilometros',
        'vei_preco_venda',
        'vei_estado',
    )
    list_filter = ('vei_estado', 'vei_ano', 'vei_mdl__mdl_mrc', 'vei_cmb')
    search_fields = (
        'vei_matricula',
        'vei_vin',
        'vei_mdl__mdl_nome',
        'vei_mdl__mdl_mrc__mrc_nome',
    )


@admin.register(ImagemVeiculo)
class ImagemVeiculoAdmin(admin.ModelAdmin):
    list_display = ('img_id', 'img_vei', 'img_caminho', 'img_capa', 'img_criado_em')
    list_filter = ('img_capa',)


@admin.register(FinanciamentoVeiculo)
class FinanciamentoVeiculoAdmin(admin.ModelAdmin):
    list_display = ('fin_id', 'fin_vei', 'fin_prazo_meses', 'fin_prestacao')
    list_filter = ('fin_prazo_meses',)


@admin.register(Utilizador)
class UtilizadorAdmin(admin.ModelAdmin):
    list_display = ('usr_id', 'usr_nome', 'usr_email', 'usr_tipo', 'usr_criado_em')
    search_fields = ('usr_nome', 'usr_email')
    list_filter = ('usr_tipo',)


@admin.register(SimulacaoCredito)
class SimulacaoCreditoAdmin(admin.ModelAdmin):
    list_display = ('sim_id', 'sim_usr', 'sim_vei', 'sim_prazo_meses', 'sim_prestacao', 'sim_criado_em')
    list_filter = ('sim_prazo_meses', 'sim_criado_em')


@admin.register(TestDrive)
class TestDriveAdmin(admin.ModelAdmin):
    list_display = ('tdr_id', 'tdr_usr', 'tdr_vei', 'tdr_data', 'tdr_hora', 'tdr_estado')
    list_filter = ('tdr_estado', 'tdr_data')