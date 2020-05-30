#from .models import Usuarios
from django import forms
from django.contrib.auth.models import User
from .models import Pedido, Produto, Usuario, FormaPagamento, Carrinho, Tipo, Bairro, Endereco

class UserModelForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'password', 'email', 'telefone']

    def save(self, commit=True):
        user = super(UserModelForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class ProdutoModelForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome']

class PagamentoModelForm(forms.Form):
    pk_forma = forms.IntegerField()

class QuantidadeModelForm(forms.ModelForm):
    class Meta:
        model = Carrinho
        fields = ['quantidade']

class AtualizaPedido(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cod_pedido', 'status']


'''REFERENTES A ÁREA ADM'''
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'ingredientes', 'descricao', 'valor', 'cod_tipo', 'imagem']

class TipoProdutos(forms.ModelForm):
    class Meta:
        model = Tipo
        fields = ('tipo', )

class FormaPagamentoModel(forms.ModelForm):
    class Meta:
        model = FormaPagamento
        fields = ('forma', )

class TaxasModel(forms.ModelForm):
    class Meta:
        model = Bairro
        fields = '__all__'

class EnderecoModel(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = '__all__'

class EnderecoClienteModel(forms.Form):
    '''ISSO É UTIL PARA QUANDO FOR PEGAR PK DE ALGO'''
    pk = forms.IntegerField()


