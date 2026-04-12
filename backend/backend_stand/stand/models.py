from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Combustivel(models.Model):
    cmb_id = models.AutoField(primary_key=True)
    cmb_nome = models.CharField(unique=True, max_length=30)

    class Meta:
        db_table = 'combustivel'
        verbose_name = 'Combustível'
        verbose_name_plural = 'Combustíveis'

    def __str__(self):
        return self.cmb_nome


class Marca(models.Model):
    mrc_id = models.AutoField(primary_key=True)
    mrc_nome = models.CharField(unique=True, max_length=80)

    class Meta:
        db_table = 'marca'
        verbose_name = 'Marca'
        verbose_name_plural = 'Marcas'

    def __str__(self):
        return self.mrc_nome


class Modelo(models.Model):
    mdl_id = models.AutoField(primary_key=True)
    mdl_mrc = models.ForeignKey(Marca, on_delete=models.CASCADE, db_column='mdl_mrc_id')
    mdl_nome = models.CharField(max_length=100)

    class Meta:
        db_table = 'modelo'
        unique_together = (('mdl_mrc', 'mdl_nome'),)
        verbose_name = 'Modelo'
        verbose_name_plural = 'Modelos'

    def __str__(self):
        return f"{self.mdl_mrc.mrc_nome} {self.mdl_nome}"


class Utilizador(models.Model):
    usr_id = models.AutoField(primary_key=True)
    usr_nome = models.CharField(max_length=100)
    usr_email = models.EmailField(unique=True, max_length=150)
    usr_password = models.CharField(max_length=255)
    usr_telefone = models.CharField(max_length=20, blank=True, null=True)
    usr_tipo = models.CharField(max_length=20, default='cliente')
    usr_criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'utilizador'
        verbose_name = 'Utilizador'
        verbose_name_plural = 'Utilizadores'

    def __str__(self):
        return self.usr_nome


class Veiculo(models.Model):
    vei_id = models.AutoField(primary_key=True)
    vei_mdl = models.ForeignKey(Modelo, on_delete=models.CASCADE, db_column='vei_mdl_id')
    vei_cmb = models.ForeignKey(
        Combustivel,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        db_column='vei_cmb_id'
    )
    vei_matricula = models.CharField(unique=True, max_length=20)
    vei_vin = models.CharField(unique=True, max_length=50)
    vei_versao = models.CharField(max_length=120, blank=True, null=True)
    vei_importado = models.BooleanField(default=False)

    vei_mes = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(1), MaxValueValidator(12)]
    )

    vei_ano = models.IntegerField(
        validators=[MinValueValidator(1900), MaxValueValidator(2100)]
    )

    vei_quilometros = models.IntegerField(
        validators=[MinValueValidator(0)]
    )

    vei_cilindrada = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)]
    )

    vei_potencia_cv = models.IntegerField(
        blank=True,
        null=True,
        validators=[MinValueValidator(0)]
    )

    vei_preco_venda = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)]
    )

    vei_estado = models.CharField(max_length=30, default='Disponível')
    vei_descricao = models.TextField(blank=True, null=True)
    vei_criado_em = models.DateTimeField(auto_now_add=True)
    vei_atualizado_em = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'veiculo'
        verbose_name = 'Veículo'
        verbose_name_plural = 'Veículos'

    def __str__(self):
        return f"{self.vei_mdl} - {self.vei_matricula}"


class ImagemVeiculo(models.Model):
    img_id = models.AutoField(primary_key=True)
    img_vei = models.ForeignKey(Veiculo, on_delete=models.CASCADE, db_column='img_vei_id')
    img_caminho = models.CharField(max_length=255)
    img_capa = models.BooleanField(default=False)
    img_criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'imagem_veiculo'
        verbose_name = 'Imagem do Veículo'
        verbose_name_plural = 'Imagens dos Veículos'

    def __str__(self):
        return self.img_caminho


class FinanciamentoVeiculo(models.Model):
    fin_id = models.AutoField(primary_key=True)
    fin_vei = models.ForeignKey(Veiculo, on_delete=models.CASCADE, db_column='fin_vei_id')
    fin_prazo_meses = models.IntegerField()
    fin_tan = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    fin_taeg = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    fin_entrada_inicial = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fin_imposto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fin_montante_total = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fin_prestacao = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    fin_criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'financiamento_veiculo'
        verbose_name = 'Financiamento do Veículo'
        verbose_name_plural = 'Financiamentos dos Veículos'

    def __str__(self):
        return f"Financiamento {self.fin_vei}"


class SimulacaoCredito(models.Model):
    sim_id = models.AutoField(primary_key=True)
    sim_usr = models.ForeignKey(Utilizador, on_delete=models.CASCADE, db_column='sim_usr_id')
    sim_vei = models.ForeignKey(Veiculo, on_delete=models.CASCADE, db_column='sim_vei_id')
    sim_entrada = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sim_taxa = models.DecimalField(max_digits=6, decimal_places=3, blank=True, null=True)
    sim_prazo_meses = models.IntegerField()
    sim_prestacao = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    sim_criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'simulacao_credito'
        verbose_name = 'Simulação de Crédito'
        verbose_name_plural = 'Simulações de Crédito'

    def __str__(self):
        return f"Simulação {self.sim_id}"


class TestDrive(models.Model):
    tdr_id = models.AutoField(primary_key=True)
    tdr_usr = models.ForeignKey(Utilizador, on_delete=models.CASCADE, db_column='tdr_usr_id')
    tdr_vei = models.ForeignKey(Veiculo, on_delete=models.CASCADE, db_column='tdr_vei_id')
    tdr_data = models.DateField()
    tdr_hora = models.TimeField()
    tdr_estado = models.CharField(max_length=30, default='Pendente')
    tdr_observacoes = models.TextField(blank=True, null=True)
    tdr_criado_em = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'test_drive'
        verbose_name = 'Test Drive'
        verbose_name_plural = 'Test Drives'

    def __str__(self):
        return f"Test Drive {self.tdr_id}"