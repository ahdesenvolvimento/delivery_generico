#from .models import Usuarios
from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
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

class CarrinhoModelForm(forms.ModelForm):
    '''
    quantidade = forms.IntegerField(
        label='Quantidade',
        required=True
    )
    observacao = forms.CharField(
        label='Observações',
        required=True,
        max_length=100,
        widget=forms.TextInput()
    )
    def clean_observacao(self):
        data = self.cleaned_data['observacao']
        if 'carlos' not in data:
            print("sem carlinhos")
            raise forms.ValidationError('Tek qe ter o carls')
        return data
    '''
    class Meta:
        model = Carrinho
        fields = ['quantidade', 'observacao']

    def clean_observacao(self):
        data = self.cleaned_data['observacao']
        if 'carlos' not in data:
            print("sem carlinhos")
            raise forms.ValidationError('Tek qe ter o carls')
        return data

class AtualizaPedido(forms.ModelForm):
    class Meta:
        model = Pedido
        fields = ['cod_pedido', 'status']


'''REFERENTES A ÁREA ADM'''
class ProdutoForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome', 'ingredientes', 'descricao', 'valor', 'cod_tipo', 'imagem']
        error_messages = {
            'nome':{
                'required':'Campo obrigatório'
            },
            'ingredientes':{
                'required':'Campo obrigatório'
            },
            'valor': {
                'required': 'Campo obrigatório'
            },
            'descricao': {
                'required': 'Campo obrigatório'
            }
        }

    def clean_nome(self):
        dados = self.cleaned_data['nome']
        produto = Produto.objects.filter(nome=dados)
        if produto:
            raise forms.ValidationError('Este produto já está cadastrado no sistema')
        return dados

    def clean_valor(self):
        dados = self.cleaned_data['valor']
        if dados <= 0:
            raise forms.ValidationError('Apenas valores positivos')
        return dados

class TipoProdutos(forms.ModelForm):
    class Meta:
        model = Tipo
        fields = ['tipo']
        widgets = {
            'tipo':forms.TextInput(attrs={
                'class':'form-control',
                'maxlength':60,
                'placeholder':'Tipo',
                'id':'tipo',
                'name':'tipo'
            })
        }
        error_messages = {
            'tipo': {
                'required':'Obrigatorio ai parceiro',
                'max_length':'Você só pode colocar no máximo 50 digitos'
                }
        }

    def clean_tipo(self):
        data = self.cleaned_data['tipo']
        dados = Tipo.objects.filter(tipo=data)
        if data:
            raise forms.ValidationError('Este tipo de produto já está cadastrado no sistema')
        return data

class FormaPagamentoModel(forms.ModelForm):
    class Meta:
        model = FormaPagamento
        fields = ['forma']
        '''
        widgets = {
            'forma':forms.TextInput(attrs={
                'class':'form-control',
                'maxlength':15,
                'name':'forma',
                'id':'forma'
            })
        }
        '''
        error_messages = {
            'forma': {
                'required':'Campo obrigatório'
            }
        }
    def clean_forma(self):
        dados = self.cleaned_data['forma']
        formas = FormaPagamento.objects.filter(forma=dados)
        if formas:
            raise forms.ValidationError('Está forma de pagamento já existe no sistema')
        return dados

class TaxasModel(forms.ModelForm):
    class Meta:
        model = Bairro
        fields = '__all__'
        widgets = {
            'taxa':forms.NumberInput(attrs={'class':'form-control',
                                            'id':'taxa',
                                            'name':'taxa'}),
            'nome':forms.TextInput(attrs={'class':'form-control',
                                          'maxlength':30,
                                          'id':'nome',
                                          'name':'nome'})
        }
        error_messages = {
            'taxa': {
                'required':'Campo obrigatório'
            },
            'nome': {
                'required':'Campo obrigatório'
            }
        }

    def clean_taxa(self):
        data = self.cleaned_data['taxa']
        if data <= 0:
            raise forms.ValidationError('Apenas valores positivos!')
        return data

    def clean_nome(self):
        data = self.cleaned_data['nome']
        dados = Bairro.objects.filter(nome=data)
        if data:
            raise forms.ValidationError('Já existe um bairro com este nome no sistema')
        return data

class EnderecoModel(forms.ModelForm):
    class Meta:
        model = Endereco
        fields = ['numero_casa', 'bairro', 'cep', 'complemento', 'ponto']
        exclude = ['cod_cliente']

    def save(self, commit=True):
        user = super(EnderecoModel, self).save(commit=False)
        user.cod_cliente = username
        if commit:
            user.save()
        return user

class EnderecoClienteModel(forms.Form):
    '''ISSO É UTIL PARA QUANDO FOR PEGAR PK DE ALGO'''
    pk = forms.IntegerField()


