from django.contrib import admin
from .models import Produto, Pedido, Tipo, Carrinho, FormaPagamento, Usuario, Bairro
from django.contrib.auth.admin import UserAdmin

@admin.register(Usuario)
class UAdmin(UserAdmin):

    list_display = ['is_staff', 'controle_pedido']


@admin.register(Produto)
class ProdAdmin(admin.ModelAdmin):
    
    list_display = ['nome', 'descricao', 'valor', 'tipo']

    def tipo(self, instance):
        return instance.cod_tip.tipo

@admin.register(Tipo)
class PrimarioAdmin(admin.ModelAdmin):

    list_display = ['cod_tipo', 'tipo']

@admin.register(Pedido)
class CompraAdmin(admin.ModelAdmin):

    list_display = ['status', 'cod_forma', 'total', 'nome']

    def nome(self, instance):
        return instance.cod_carrinho.cod_cliente.username

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

'''
@admin.register(Carrinho)
class CarrinhoAdmin(admin.ModelAdmin):
    list_display = ['cod_pseudo_pedido', 'cod_prod', 'quantidade', 'total']
'''
@admin.register(Bairro)
class BairroAdmin(admin.ModelAdmin):
    list_display = ['nome', 'taxa']
'''
@admin.register(BasePedido)
class BaseAdmin(admin.ModelAdmin):
    list_display = ['nome', 'finalizado']

    def nome(self, instance):
        return instance.cod_cliente.username
'''

