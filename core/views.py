from django.shortcuts import render, redirect, get_object_or_404
#from .models import Usuarios
from .models import Tipo, Produto, Pedido, Carrinho, FormaPagamento, Bairro, Usuario, EnderecoCliente, Endereco
from .forms import UserModelForm, ProdutoModelForm,\
    PagamentoModelForm, CarrinhoModelForm, AtualizaPedido,\
    ProdutoForm, TipoProdutos, FormaPagamentoModel, TaxasModel, \
    EnderecoModel, EnderecoClienteModel

from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
# Create your views here.

def index(request):
    if request.user.is_staff:
        pedidos = Pedido.objects.all().order_by('-cod_pedido')
        produtos = Carrinho.objects.all()
       # with connection.cursor() as cursor:
         #   cursor.execute(
           #     'SELECT USERNAME, COD_PEDIDO, STATUS, NOME FROM CORE_PEDIDO INNER JOIN CORE_BASEPEDIDO ON COD_CARRINHO_ID = COD_BASE INNER JOIN CORE_CARRINHO ON COD_PSEUDO_PEDIDO_ID = COD_BASE INNER JOIN CORE_PRODUTO ON COD_PROD_ID = COD_PROD INNER JOIN CORE_USUARIO ON COD_CLIENTE_ID = ID'
          #  )
          #  pedidos = cursor.fetchall()
       # print(pedidos[0])

        form = AtualizaPedido(request.POST or None)

        if form.is_valid():# and form2.is_valid():
            print(form.cleaned_data)
            #print(form2.cleaned_data)
            pedido = Pedido.objects.filter(cod_pedido=request.POST.get('cod_pedido')).update(status=form.cleaned_data['status'])
            print(request.POST.get("cod_pseudo_pedido"))
            print('ops')
        else:
            print('haha')
        return render(request, 'index.html', {'pedidos':pedidos,
                                              'produtos':produtos})

    else:
        if str(request.method == 'POST'):
            tipo = Tipo.objects.all()
            produtos = Produto.objects.all()
            print('começo')
            form_produto = ProdutoModelForm(request.POST)
            form_carrinho = CarrinhoModelForm(request.POST)
            if form_produto.is_valid() and form_carrinho.is_valid():
                print('formulario')
                dados_prod = form_produto.cleaned_data
                dados_carrinho = form_carrinho.cleaned_data
                prod = Produto.objects.get(nome=dados_prod['nome'])
                try:
                    print('try')
                    carro = Carrinho.objects.get(cod_cliente=request.user.id,
                                                 cod_pedido=None,
                                                 cod_cliente__controle_pedido=True,
                                                 cod_prod__nome=dados_prod['nome'])
                    print(carro)
                    #existe = Carrinho.objects.filter(cod_pseudo_pedido=variavel.cod_base,
                    #                                 cod_pseudo_pedido__cod_cliente=request.user.id,
                    #
                    #                                 cod_prod__nome=dados_prod['nome'])

                    with connection.cursor() as cursor:
                        cursor.execute(
                            'SELECT NOME, QUANTIDADE, VALOR FROM CORE_PRODUTO P INNER JOIN CORE_CARRINHO C ON P.COD_PROD = C.COD_PROD_ID INNER JOIN CORE_USUARIO U ON COD_CLIENTE_ID = U.ID WHERE U.ID = %s AND CONTROLE_PEDIDO = %s AND NOME = %s',
                            (request.user.id, True, dados_prod['nome']))
                        linhas = cursor.fetchall()
                    quantidade = linhas[0][1] + dados_carrinho['quantidade']
                    total = quantidade * linhas[0][2]
                    atualiza_carrinho = Carrinho.objects.filter(cod_pedido=None,
                                                                cod_cliente=request.user.id,
                                                                cod_cliente__controle_pedido=True,
                                                                cod_prod__nome=dados_prod['nome']).update(quantidade=quantidade,
                                                                                                          total=total,
                                                                                                          observacao=dados_carrinho['observacao'])

                    #else:
                      #  inserir = Carrinho.objects.create(cod_pseudo_pedido=variavel,
                         #                                 cod_prod=prod,
                           #                               quantidade=dados_quantidade['quantidade'],
                            #                              total=prod.valor * dados_quantidade['quantidade'])

                except ObjectDoesNotExist:
                    print('entrei aqui except')
                   # base = BasePedido.objects.create(cod_cliente=request.user,
                    #                                 controle=True)
                   # base.save()
                    total = prod.valor * dados_carrinho['quantidade']
                    print('aqui carrinho')
                    carrinho = Carrinho.objects.create(cod_prod=prod,
                                                       quantidade=dados_carrinho['quantidade'],
                                                       cod_cliente=request.user,
                                                       total=total,
                                                       observacao=dados_carrinho['observacao'])
                    usuario = Usuario.objects.filter(id=request.user.id).update(controle_pedido=True)
                    carrinho.save()

            carrinho = Carrinho.objects.filter(cod_cliente=request.user.id,
                                               cod_pedido=None)
            print(carrinho)
            return render(request,
                          'index.html',
                          {'tipo':tipo,
                           'produtos':produtos,
                           'carrinho':carrinho})
                        #    form_carrinho
                          #  ':form_carrinho})
                          # 'base':variavel})

def cadastro(request):
    form = UserModelForm(request.POST or None)
    bairros = Bairro.objects.all()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('contas/login')
    return render(request, 'cadastro.html', {'bairro':bairros})

def pedidos(request):
    pedidos = Pedido.objects.filter(cod_endereco__cod_cliente=request.user.id).order_by('-cod_pedido')
    produtos = Carrinho.objects.filter(cod_cliente=request.user.id)
    #print(produtos)
    #produtos = Carrinho.objects.filter(cod_pedido__cod_cliente=request.user.id)
    #bairro = Usuario.objects.get(id=request.user.id)
   # taxa = Bairro.objects.get(nome=bairro.bairro)
   # with connection.cursor() as cursor:
    ##    cursor.execute(
       #     'SELECT COD_COMPRA, SUM(TOTAL)+%s FROM CORE_PRODUTOPEDIDO INNER JOIN CORE_PRODUTO ON COD_PROD_ID = COD_ING INNER JOIN CORE_PEDIDO ON COD_PEDIDO_ID = COD_COMPRA INNER JOIN CORE_USUARIO ON COD_CLIENTE_ID = ID WHERE CORE_USUARIO.ID = %s GROUP BY COD_COMPRA ORDER BY COD_COMPRA DESC',
    #       (taxa.taxa,
       #      request.user.id,))
       # total = cursor.fetchall()

    return render(request, 'pedidos.html', {'pedidos':pedidos,
                                            'produtos':produtos})#, 'produtos':produtos, 'total':total})

def finalizar(request):
    forma = FormaPagamento.objects.all()
    form_pagamento = PagamentoModelForm(request.POST or None)
    endereco_form = EnderecoModel(request.POST or None)
    dados = EnderecoClienteModel(request.POST or None)
    if form_pagamento.is_valid() and dados.is_valid():
        dados_forma = form_pagamento.cleaned_data
        dados_bairro = dados.cleaned_data
        #print(dados_forma['pk_forma'])
        total = Carrinho.objects.filter(cod_pedido=None,
                                        cod_cliente=request.user.id,
                                        cod_cliente__controle_pedido=True).aggregate(Sum('total'))
        print(total)

        forma_pagamento = FormaPagamento.objects.get(cod_forma=dados_forma['pk_forma'])
        dados_endereco_cliente = Endereco.objects.get(cod_endereco=dados_bairro['pk'])#, #cod_cliente=request.user.id)
        endereco_cliente = EnderecoCliente.objects.create(cod_cliente=request.user,
                                                          cod_endereco=dados_endereco_cliente)
        pedido = Pedido.objects.create(cod_forma=forma_pagamento,
                                       total=total['total__sum'] + dados_endereco_cliente.bairro.taxa,
                                       status='Aguardando confirmação',
                                       cod_endereco=endereco_cliente)
        atualiza_carrinho = Carrinho.objects.filter(cod_pedido=None,
                                                    cod_cliente=request.user.id,
                                                    cod_cliente__controle_pedido=True).update(cod_pedido=pedido)
        atualiza_usuario = Usuario.objects.filter(id=request.user.id,
                                                  controle_pedido=True).update(controle_pedido=False)
        return redirect('index')

        #print(total['total__sum'] + total2.bairro.taxa)
    if endereco_form.is_valid():
        dados_endereco = endereco_form.cleaned_data
        endereco = Endereco.objects.create(numero_casa=dados_endereco['numero_casa'],
                                           bairro=dados_endereco['bairro'],
                                           cep=dados_endereco['cep'],
                                           complemento=dados_endereco['complemento'],
                                           ponto=dados_endereco['ponto'],
                                           cod_cliente=request.user)
        endereco.save()
        print('41241')
    else:
        print('not valid')
    #endereco_cliente = EnderecoCliente.objects.create(cod_cliente=request.user,
   #                                                   cod_endereco=numero)
    carrinho = Carrinho.objects.filter(cod_pedido=None,
                                       cod_cliente=request.user.id,
                                       cod_cliente__controle_pedido=True)
    #enderecos = Endereco.objects.filter(cod_cliente=request.user.id)
    enderecos = Endereco.objects.all()
    taxas = Bairro.objects.all()
    return render(request, 'finalizar.html', {'carrinho':carrinho,
                                              'forma':forma,
                                              'enderecos':enderecos,
                                              'form':endereco_form,
                                              'taxas':taxas})#,
                  #{'carrinho':carrinho,
                  # 'forma':forma})

def taxas(request):
    if request.user.is_staff:
        #request.method
        form = TaxasModel(request.POST or None)

        if form.is_valid():
            form.save()
        taxas = Bairro.objects.all()

        return render(request, 'taxas.html', {'taxas': taxas,
                                              'form':form})
    else:
        taxas = Bairro.objects.all()
        return render(request, 'taxa.html', {'taxas':taxas})

def deletar(request, pk):
    produto = Carrinho.objects.filter(cod_prod__cod_prod=pk,
                                      cod_cliente=request.user.id,
                                      cod_pedido=None)
    produto.delete()
    carrinho = Carrinho.objects.filter(cod_pedido=None,
                                       cod_cliente=request.user.id,
                                       cod_cliente__controle_pedido=True)
    if carrinho:
        return redirect('finalizar')
    else:
        return redirect('index')



'''Funções da área ADM'''
def produtos(request):
    print("21312321", request.FILES)
    form = ProdutoForm(request.POST, request.FILES)
    if form.is_valid():
        form.save()
        print('hmmm')
    else:
        print('erro')
    produtos = Produto.objects.all()
    tipos = Tipo.objects.all()
    return render(request, 'produtos.html', {'produtos':produtos,
                                             'tipos':tipos,
                                             'form':form})

def deletar_produto(request, pk):
    produto = Produto.objects.filter(cod_prod=pk)
    produto.delete()

    return redirect('produtos')

def tipos_produtos(request):
    form = TipoProdutos(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            form.save()
    else:
        form = TipoProdutos()
    tipos = Tipo.objects.all()

    return render(request, 'tipos.html', {'tipos':tipos, 'form':form})

def deletar_tipo(request, pk):
    tipo = Tipo.objects.filter(cod_tipo=pk)
    tipo.delete()

    return redirect('tipos_produtos')

def tipos_pagamento(request):
    form = FormaPagamentoModel(request.POST or None)

    if form.is_valid():
        form.save()
    formas = FormaPagamento.objects.all()

    return render(request, 'tipos_pagamento.html', {'formas':formas,
                                                    'form':form})

def deletar_forma(request, pk):
    forma = FormaPagamento.objects.filter(cod_forma=pk)
    forma.delete()

    return redirect('tipos_pagamento')

def deletar_taxa(request, pk):
    taxa = Bairro.objects.filter(cod_bairro=pk)
    taxa.delete()

    return redirect('taxas')