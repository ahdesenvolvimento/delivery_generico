from django.shortcuts import render, redirect, get_object_or_404
#from .models import Usuarios
from datetime import date

from .models import Tipo, Produto, Pedido, Carrinho, FormaPagamento, Bairro, Usuario, EnderecoCliente, Endereco, \
    MotoBoy, Adicionais #,Promocao
from .forms import UserModelForm, ProdutoModelForm,\
    PagamentoModelForm, CarrinhoModelForm, AtualizaPedido,\
    ProdutoForm, TipoProdutos, FormaPagamentoModel, TaxasModel, \
    EnderecoModel, EnderecoClienteModel, IngredientePk, \
    MotoBoyModel, MotoBoyPk, AtualizaTaxa, AdicionaisModel, AdicionaisModelCliente

from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
# Create your views here.

def index(request):
    if request.user.is_staff:
        return redirect('administracao')
    else:
        if str(request.method == 'POST'):
            tipo = Tipo.objects.all()

            produtos = Produto.objects.filter(ativo=True)
            adicionais = Adicionais.objects.filter(ativo=True)

            form_produto = ProdutoModelForm(request.POST)
            form_carrinho = CarrinhoModelForm(request.POST)
            if form_produto.is_valid() and form_carrinho.is_valid():
                print('formulario')
                dados_prod = form_produto.cleaned_data
                dados_carrinho = form_carrinho.cleaned_data
                print(dados_carrinho)
                prod = Produto.objects.get(nome=dados_prod['nome'])

                try:
                    print('try')
                    carro = Carrinho.objects.get(cod_cliente=request.user.id,
                                                 cod_pedido=None,
                                                 cod_cliente__controle_pedido=True,
                                                 cod_prod__nome=dados_prod['nome'])
                    print(carro)

                    with connection.cursor() as cursor:
                        cursor.execute(
                            'SELECT NOME, QUANTIDADE, VALOR FROM CORE_PRODUTO P INNER JOIN CORE_CARRINHO C ON P.COD_PROD = C.COD_PROD_ID INNER JOIN CORE_USUARIO U ON COD_CLIENTE_ID = U.ID WHERE U.ID = %s AND CONTROLE_PEDIDO = %s AND NOME = %s AND C.COD_PEDIDO_ID IS NULL',
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
                    total = prod.valor * dados_carrinho['quantidade']

                    carrinho = Carrinho.objects.create(cod_prod=prod,
                                                       quantidade=dados_carrinho['quantidade'],
                                                       cod_cliente=request.user,
                                                       total=total,
                                                       observacao=dados_carrinho['observacao'])

                    usuario = Usuario.objects.filter(id=request.user.id).update(controle_pedido=True)
                    carrinho.save()


            else:
                print('form invalido')
            carrinho = Carrinho.objects.filter(cod_cliente=request.user.id,
                                               cod_pedido=None)

           # print(carrinho)
            return render(request,
                          'index.html',
                          {'tipo':tipo,
                           'produtos':produtos,
                           'carrinho':carrinho})#,
                          # 'x':pk_ing})
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
    return render(request, 'cadastro.html', {'bairro':bairros,
                                             'form':form})

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
        #atualiza_adicional = Adicionais.objects.filter(cod_carrinho__cod_cliente=request.user).update(cod_pedido=pedido)
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
                                              'taxas':taxas,
                                              'dados':dados,
                                              'forma_validado':form_pagamento})#,
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

def deletar_produto_carrinho_index(request, pk):
    produto = Carrinho.objects.filter(cod_prod__cod_prod=pk,
                                      cod_cliente=request.user.id,
                                      cod_pedido=None)
    produto.delete()
    carrinho = Carrinho.objects.filter(cod_pedido=None,
                                       cod_cliente=request.user.id,
                                       cod_cliente__controle_pedido=True)
    return redirect('index')

'''Funções da área ADM'''

def administracao(request):
    data_atual = date.today()
    pedidos = Pedido.objects.all().filter(modificacao=data_atual).order_by('-cod_pedido')
    pk_moto = MotoBoyPk(request.POST or None)
    motoboy = MotoBoy.objects.all()
    produtos = Carrinho.objects.all()
    adicionais = Adicionais.objects.all()
    # with connection.cursor() as cursor:
    #   cursor.execute(
    #     'SELECT USERNAME, COD_PEDIDO, STATUS, NOME FROM CORE_PEDIDO INNER JOIN CORE_BASEPEDIDO ON COD_CARRINHO_ID = COD_BASE INNER JOIN CORE_CARRINHO ON COD_PSEUDO_PEDIDO_ID = COD_BASE INNER JOIN CORE_PRODUTO ON COD_PROD_ID = COD_PROD INNER JOIN CORE_USUARIO ON COD_CLIENTE_ID = ID'
    #  )
    #  pedidos = cursor.fetchall()
    # print(pedidos[0])

    form = AtualizaPedido(request.POST or None)
    if pk_moto.is_valid():
        dados_moto = pk_moto.cleaned_data
        moto = MotoBoy.objects.get(cod_moto=dados_moto['pk_moto'])
        pedido = Pedido.objects.filter(cod_pedido=request.POST.get('cod_pedido')).update(cod_motoboy=moto)


    if form.is_valid():## and pk_moto.is_valid():  # and form2.is_valid():
       #
        pedido = Pedido.objects.filter(cod_pedido=request.POST.get('cod_pedido')).update(
            status=form.cleaned_data['status'])#, cod_motoboy=moto)
    else:
        print('haha')
    return render(request, 'administracao.html', {'pedidos':pedidos,
                                                  'produtos':produtos,
                                                  'motoboys':motoboy,
                                                  'adicionais':adicionais})

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

def ingredientes(request):
    ing = IngredientesModel(request.POST or None)
    x = Ingredientes.objects.all()
    if ing.is_valid():
        print('deu certo')
        ing.save()
    return render(request, 'ingredientes.html', {'form':ing, 'x':x})

def motoboy(request):
    moto = MotoBoyModel(request.POST or None)
    motos = MotoBoy.objects.all()
    if moto.is_valid():
        moto.save()
    return render(request, 'motoboy.html', {'form':moto, 'x':motos})
'''

def promocao(request):
    promo = PromocaoModel(request.POST or None)
    promocoes = Promocao.objects.all()
    produtos = Produto.objects.filter(ativo=True)
    if promo.is_valid():
        dados = promo.cleaned_data['produto']

        produto = Produto.objects.filter(nome=dados).update(ativo=False)
        print(produto)
        print(dados)
        promo.save()
    return render(request, 'promocao.html', {'form':promo, 'promocoes':promocoes, 'produtos':produtos})
'''

def atualiza_produto(request, pk):
    produto = Produto.objects.get(cod_prod=pk)
    prod = ProdutoForm(request.POST or None, instance=produto)
    if prod.is_valid():
        prod.save()
        return redirect('produtos')
    return render(request, 'produto.html', {'produto':produto, 'form':prod})

def atualiza_bairro(request, pk):
    bairro = Bairro.objects.get(cod_bairro=pk)
    taxa = AtualizaTaxa(request.POST or None, instance=bairro)
    if taxa.is_valid():
        taxa.save()
        return redirect('taxas')
    return render(request, 'atualiza_bairro.html', {'bairro':bairro, 'form':taxa})

'''
def atualiza_promocao(request, pk):
    promocao = Promocao.objects.get(cod_promo=pk)
    promo = PromocaoModel(request.POST or None, instance=promocao)
    if promo.is_valid():
        dados = promo.cleaned_data
        if dados['ativo'] is True:
            produto = Produto.objects.filter(nome=dados['produto']).update(ativo=False)
        else:
            produto = Produto.objects.filter(nome=dados['produto']).update(ativo=True)
        print("dADOS", dados)
        promo.save()
        return redirect('promocao')
    return render(request, 'atualiza_promocao.html', {'form':promo})

def deletar_promocao(request, pk):
    promo = Promocao.objects.get(cod_promo=pk)
    print(promo.ativo)
    if promo.ativo is True:
        print('entrie aqui')
        promocao = Promocao.objects.filter(cod_promo=pk).update(ativo=False)
        produto = Produto.objects.filter(nome=promo.produto).update(ativo=True)
        promo = Promocao.objects.filter(cod_promo=pk)
        promo.delete()
    else:
        promo = Promocao.objects.filter(cod_promo=pk)
        promo.delete()

    return redirect('promocao')
'''
def adicionais(request):
    adicional = AdicionaisModel(request.POST)
    ad = Adicionais.objects.all()
    if adicional.is_valid():
        adicional.save()
    return render(request, 'adicionais.html', {'form':adicional, 'adicional':ad})