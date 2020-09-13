from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from stdimage.models import StdImageField
# Create your models here.

class BaseManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, password, **extra_fields):
        if not username:
            raise ValueError('O nome deve ser informado')

        username = self.model.normalize_username(username)
        user = self.model(username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, password, **extra_fields)

    def create_superuser(self, username, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser tem que ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser tem que ter is_superuser=True.')
        return self._create_user(username, password, **extra_fields)

class Bairro(models.Model):
    cod_bairro = models.AutoField('Código do bairro', primary_key=True)
    nome = models.CharField('Nome do bairro', max_length=30)
    taxa = models.FloatField('Taxa de entrega')

    class Meta:
        verbose_name = 'Bairro'
        verbose_name_plural = 'Bairros'
    def __str__(self):
        return self.nome

class Usuario(AbstractUser):
    username = models.CharField('Telefone', max_length=25, unique=True)
    controle_pedido = models.BooleanField('Pedido finalizado?', default=False)

    is_staff = models.BooleanField('Membro da equipe', default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email']
    objects = BaseManager()

class Endereco(models.Model):
    cod_endereco = models.AutoField('Código', primary_key=True)
    numero_casa = models.IntegerField('Número')
    cep = models.CharField('CEP', max_length=50)
    complemento = models.CharField('Complemento', max_length=100)
    ponto = models.CharField('Ponto de referência', max_length=50, default=None)
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE)
    cod_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=None, null=True)

class EnderecoCliente(models.Model):
    cod_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    cod_endereco = models.ForeignKey(Endereco, on_delete=models.CASCADE)

class Base(models.Model):
    criacao = models.DateTimeField('Criação', auto_now_add=True)
    modificacao = models.DateField('Modificação', auto_now=True)

    class Meta:
        abstract = True

class Tipo(models.Model):
    cod_tipo = models.AutoField('Código do tipo do produto', primary_key=True)
    tipo = models.CharField('Tipo', max_length=50)
    ativo = models.BooleanField('Ativo', default=False, null=True, blank=False)

    def __str__(self):
        return self.tipo

class Produto(models.Model):
    cod_prod = models.AutoField('Código do produto', primary_key=True)
    nome = models.CharField('Nome do produto', max_length=50)
    ingredientes = models.CharField('Ingredientes', max_length=50)
    descricao = models.TextField('Descrição do produto', max_length=120)
    valor = models.FloatField('Preço')
    imagem = StdImageField('Imagem', upload_to='produtos', variations={'thumb':(124,124)})
    ativo = models.BooleanField('Ativo', default=True, null=True, blank=False)
    cod_tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome


class Adicionais(models.Model):
    cod_adicional = models.AutoField('Código do adicional', primary_key=True)
    nome = models.CharField('Nome do adicional', max_length=20, blank=False, null=False)
    valor = models.FloatField('Valor em R$', blank=False, null=False)
    ativo = models.BooleanField('Ativo', default=True, null=True, blank=False)

'''
class AdicionalProduto(models.Model):
    cod_adicional_prod = models.AutoField('Código', primary_key=True)
    cod_adic = models.ForeignKey(Adicionais, on_delete=models.DO_NOTHING)
    cod_prod = models.ForeignKey(Produto, on_delete=models.DO_NOTHING)
'''
class FormaPagamento(models.Model):
    cod_forma = models.AutoField('Código', primary_key=True)
    forma = models.CharField('Forma de pagamento', max_length=75, unique=True)
    ativo = models.BooleanField('Ativo', default=False, null=True, blank=False)
    troco = models.FloatField('Troco', null=True, blank=True)
    class Meta:
        verbose_name = 'Forma de pagamento'
        verbose_name_plural = 'Formas de pagamento'
    def __str__(self):
        return self.forma

class MotoBoy(models.Model):
    cod_moto = models.AutoField("Codigo", primary_key=True)
    nome = models.CharField('Nome', max_length=15, null=False, blank=False)
    ativo = models.BooleanField('Ativo', default=False, null=True, blank=False)

class Pedido(Base):
    UNITY_CHOICES = (
        ('1', 'Delivery'),
        ('2', 'Retirada'),
        ('3', 'Consumir no local')
    )
    cod_pedido = models.AutoField('Código do pedido', primary_key=True)
    status = models.CharField('Status do pedido', max_length=70, default='Não finalizado')
    total = models.FloatField('Total em R$')
    tipo_de_entrega = models.CharField('Tipo de entrega', max_length=50, choices=UNITY_CHOICES, blank=False, null=False)

    cod_motoboy = models.ForeignKey(MotoBoy, on_delete=models.DO_NOTHING, default=None, null=True, blank=True)
    cod_endereco = models.ForeignKey(EnderecoCliente, on_delete=models.DO_NOTHING)
    cod_forma = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE, null=True)

'''
class Promocao(models.Model):
    cod_promo = models.AutoField('Código', primary_key=True)
    produto = models.ForeignKey(Produto, on_delete=models.DO_NOTHING, null=False, blank=False)
    novo_preco = models.FloatField('Novo preço', null=False, blank=False)
    ativo = models.BooleanField('Ativo', default=None, null=True, blank=True)
    dia_promo = models.CharField('dia da promoção', max_length=7, null=False, blank=False)
'''
class Carrinho(Base):
    cod = models.AutoField('Código', primary_key=True)
    #cod_prod_adicional = models.ForeignKey(AdicionalProduto, on_delete=models.DO_NOTHING)
    cod_prod = models.ForeignKey(Produto, on_delete=models.DO_NOTHING, default=None)
    cod_pedido = models.ForeignKey(Pedido, on_delete=models.PROTECT, null=True)
    cod_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=None)
   # cod_promocao = models.ForeignKey(Promocao, on_delete=models.DO_NOTHING, null=True, blank=True, default=None)
    observacao = models.TextField('Observação', max_length=75, null=True, default='Sem observações', blank=True)
    quantidade = models.IntegerField('Quantidade')
    total = models.FloatField('Total', default=None, null=True)

    class Meta:
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'

class Horario(models.Model):
    UNITY_CHOICES = (
        ('1', 'Segunda'),
        ('2', 'Terça'),
        ('3', 'Quarta'),
        ('4', 'Quinta'),
        ('5', 'Sexta'),
        ('6', 'Sábado'),
        ('7', 'Domingo'),
    )
    dia = models.CharField('Dia', choices=UNITY_CHOICES, max_length=20)
    hora_abrir = models.TimeField('Horário de abrir', blank=False, null=False)
    hora_fechar = models.TimeField('Horário de fechar', blank=False, null=False)




