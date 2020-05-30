from django.test import TestCase
from model_mommy import mommy
from core.models import Usuario, BaseManager

class UsuarioTestCase(TestCase):
    def setUp(self):
        print('Iniciando testes!')
    def test_Usuario(self):
        self.usuario = Usuario.objects.create(username='teste',
                                         email='emailg@gmail.com',
                                         telefone='12412421',
                                         numero=12412,
                                         bairro='412412',
                                         cep='42141',
                                         complemento='42141',
                                         ponto='4124',
                                            first_name='jose',
                                          last_name='carlos',
                                          password='moises')
        self.assertTrue(self.usuario.username, 'teste')

class PrimarioTest(TestCase):
    def setUp(self):
        print("Iniciando Tipo Tests")
        self.primario = mommy.make('Tipo')
    def test_str(self):
        self.assertEquals(str(self.primario), self.primario.nome)

class ProdutoTest(TestCase):
    def setUp(self):
        print("Iniciando Produto Tests")
        self.produto = mommy.make('Produto')
    def test_str(self):
        self.assertEquals(str(self.produto), self.produto.nome)

class FormaTest(TestCase):
    def setUp(self):
        print("Iniciando Forma Tests")
        self.forma = mommy.make('FormaPagamento')
    def test_str(self):
        self.assertEquals(str(self.forma), self.forma.forma)