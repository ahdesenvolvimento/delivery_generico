#from .models import Usuarios
from django import forms
from django.contrib.auth.models import User
from .models import Pedido, Teste, Produto, Usuario, FormaPagamento, ProdutoPedido

class UserModelForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['username', 'first_name', 'last_name', 'password', 'email', 'telefone', 'numero', 'bairro', 'cep', 'complemento', 'ponto']

    def save(self, commit=True):
        user = super(UserModelForm, self).save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user

class PedidoModelForm(forms.ModelForm):
    class Meta:
        model = Produto
        fields = ['nome']

class PagamentoModelForm(forms.ModelForm):
    class Meta:
        model = FormaPagamento
        fields = ['forma']

class ProdutoPedidoModelForm(forms.ModelForm):
    class Meta:
        model = ProdutoPedido
        fields = ['quantidade']