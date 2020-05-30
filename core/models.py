from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager, User
from stdimage.models import StdImageField
# Create your models here.

class BaseManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError('O nome deve ser informado')
        email = self.normalize_email(email)
        username = self.model.normalize_username(username)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(username, email, password, **extra_fields)

    def create_superuser(self, username, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser tem que ter is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser tem que ter is_superuser=True.')
        return self._create_user(username, email, password, **extra_fields)

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
    username = models.CharField('Username', max_length=25, unique=True)
    email = models.EmailField('Email', max_length=75)
    telefone = models.CharField('Telefone', max_length=15)
    controle_pedido = models.BooleanField('Pedido finalizado?', default=False)

    is_staff = models.BooleanField('Membro da equipe', default=False)
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'telefone']
    objects = BaseManager()

class Endereco(models.Model):
    numero = models.AutoField('Número', primary_key=True)
    bairro = models.ForeignKey(Bairro, on_delete=models.CASCADE)
    cep = models.CharField('CEP', max_length=50)
    complemento = models.CharField('Complemento', max_length=100)
    ponto = models.CharField('Ponto de referência', max_length=50, default=None)
    #cod_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=None, null=True)

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

    def __str__(self):
        return self.tipo

class Produto(models.Model):
    cod_prod = models.AutoField('Código do produto', primary_key=True)
    nome = models.CharField('Nome do produto', max_length=50)
    ingredientes = models.CharField('Ingredientes', max_length=50)
    descricao = models.TextField('Descrição do produto', max_length=120)
    valor = models.FloatField('Preço')
    cod_tipo = models.ForeignKey(Tipo, on_delete=models.CASCADE)
    imagem = StdImageField('Imagem', upload_to='produtos', variations={'thumb':(124,124)})

    class Meta:
        verbose_name = 'Produto'
        verbose_name_plural = 'Produtos'

    def __str__(self):
        return self.nome

class FormaPagamento(models.Model):
    cod_forma = models.AutoField('Código', primary_key=True)
    forma = models.CharField('Forma de pagamento', max_length=75, unique=True)
    class Meta:
        verbose_name = 'Forma de pagamento'
        verbose_name_plural = 'Formas de pagamento'
    def __str__(self):
        return self.forma

class Pedido(Base):
    cod_pedido = models.AutoField('Código do pedido', primary_key=True)
    status = models.CharField('Status do pedido', max_length=70, default='Não finalizado')
    cod_forma = models.ForeignKey(FormaPagamento, on_delete=models.CASCADE, null=True)
    total = models.FloatField('Total em R$')
    cod_endereco = models.ForeignKey(EnderecoCliente, on_delete=models.CASCADE)

class Carrinho(Base):
    cod = models.AutoField('Código', primary_key=True)
    cod_prod = models.ForeignKey(Produto, on_delete=models.CASCADE)
    cod_pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, null=True)
    cod_cliente = models.ForeignKey(Usuario, on_delete=models.CASCADE, default=None)
    observacao = models.TextField('Observação', max_length=75, null=True, default=None)
    quantidade = models.IntegerField('Quantidade')
   #cod_motoboy = models.ForeignKey(Motoboy, on_delete=models.CASCADE, default=None)
    total = models.FloatField('Total', default=None, null=True)

    class Meta:
        verbose_name = 'Carrinho'
        verbose_name_plural = 'Carrinhos'



