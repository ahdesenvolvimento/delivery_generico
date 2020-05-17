from django.contrib import admin
from .models import Produto, Pedido, Primario, ProdutoPedido, FormaPagamento, Usuario, Bairro
from django.contrib.auth.admin import UserAdmin

@admin.register(Usuario)
class UAdmin(UserAdmin):

    list_display = ['email', 'telefone', 'is_staff', 'bairro']

@admin.register(Produto)
class ProdAdmin(admin.ModelAdmin):

    list_display = ['nome', 'descricao', 'valor', 'tipo']

    def tipo(self, instance):
        return instance.cod_primario.nome

@admin.register(Primario)
class PrimarioAdmin(admin.ModelAdmin):

    list_display = ['cod_pri', 'nome']

@admin.register(Pedido)
class CompraAdmin(admin.ModelAdmin):

    list_display = ['status', 'cod_cliente']

    '''
    def get_queryset(self, request):
        qs = super(CompraAdmin, self).get_queryset(request)
        return qs.filter(cliente=request.user)
   
    ''''''
    def save_model(self, request, obj, form, change):
        obj.cliente = request.user
        super().save_model(request, obj, form, change)
     '''
@admin.register(FormaPagamento)
class FormaPagamentoAdmin(admin.ModelAdmin):
    list_display = ['cod_forma', 'forma']


@admin.register(ProdutoPedido)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ['cod_pedido', 'cod_prod']

@admin.register(Bairro)
class BairroAdmin(admin.ModelAdmin):
    list_display = ['nome', 'taxa']

