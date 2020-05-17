from django.shortcuts import render, redirect, get_object_or_404
#from .models import Usuarios
from .models import Primario, Produto, Pedido, ProdutoPedido, FormaPagamento, Bairro, Usuario
from .forms import UserModelForm, PedidoModelForm, PagamentoModelForm, ProdutoPedidoModelForm
from django.db import connection
from django.core.exceptions import ObjectDoesNotExist
from django.db.models import Sum
# Create your views here.

def index(request):
    with connection.cursor() as cursor:
        pedidos = Pedido.objects.filter(cod_cliente=request.user.id)
        pri = Primario.objects.all()
        produtos = Produto.objects.all()
        form = PedidoModelForm(request.POST)
        form2 = ProdutoPedidoModelForm(request.POST)
        if form.is_valid() and form2.is_valid():
            dados = form.cleaned_data
            quant = form2.cleaned_data
            prod = Produto.objects.filter(nome=dados['nome'])
            prod = prod.first()
            try:
                ped = Pedido.objects.get(cod_cliente=request.user.id, controle=True, finalizado=False)
                y = ProdutoPedido.objects.filter(cod_pedido=ped.cod_compra, cod_pedido__cod_cliente=request.user.id, cod_prod__nome=dados['nome'])
                if y:
                    cursor.execute('SELECT NOME, QUANTIDADE, VALOR FROM CORE_PRODUTOPEDIDO INNER JOIN CORE_PRODUTO ON COD_PROD_ID = COD_ING INNER JOIN CORE_PEDIDO ON COD_PEDIDO_ID = COD_COMPRA INNER JOIN CORE_USUARIO ON COD_CLIENTE_ID = ID WHERE CORE_USUARIO.ID = %s AND FINALIZADO = %s AND COD_PEDIDO_ID = %s AND NOME = %s',(request.user.id, False, ped.cod_compra, dados['nome']))
                    linhas = cursor.fetchall()

                    quantidade = linhas[0][1] + quant['quantidade']
                    total = quantidade * linhas[0][2]

                    ped = ProdutoPedido.objects.filter(cod_pedido=ped.cod_compra, cod_pedido__cod_cliente=request.user.id, cod_prod__nome=dados['nome']).update(quantidade=quantidade, total=total)
                else:
                    cursor.execute('INSERT INTO CORE_PRODUTOPEDIDO (COD_PEDIDO_ID, COD_PROD_ID, QUANTIDADE) VALUES (%s, %s, %s)', (ped.cod_compra, prod.cod_ing, quant['quantidade']))
                #pedido = ProdutoPedido.objects.create(cod_pedido=ped.cod_compra, cod_prod=prod.cod_ing, quantidade=1)
                #pedido.save()

                #total = ProdutoPedido.objects.filter(cod_pedido__cod_compra=ped.cod_compra).aggregate(Sum('cod_prod__valor'))
                #print(ped.cod_prod)
            except ObjectDoesNotExist:
                pedido = Pedido.objects.create(cod_cliente=request.user, controle=True)
                pedido.save()
                print("To aqui linha 43",prod.valor, quant['quantidade'])
                total = prod.valor * quant['quantidade']
                with connection.cursor() as cursor:
                    cursor.execute('INSERT INTO CORE_PRODUTOPEDIDO (COD_PEDIDO_ID, COD_PROD_ID, QUANTIDADE, TOTAL) VALUES (%s, %s, %s, %s)', (pedido.cod_compra, prod.cod_ing, quant['quantidade'], total))

        carrinho = ProdutoPedido.objects.filter(cod_pedido__finalizado=False,
                                                cod_pedido__cod_cliente=request.user.id)
        with connection.cursor() as cursor:
            cursor.execute(
                'SELECT COD_COMPRA, NOME, TOTAL FROM CORE_PRODUTOPEDIDO INNER JOIN CORE_PRODUTO ON COD_PROD_ID = COD_ING INNER JOIN CORE_PEDIDO ON COD_PEDIDO_ID = COD_COMPRA INNER JOIN CORE_USUARIO ON COD_CLIENTE_ID = ID WHERE CORE_USUARIO.ID = %s AND FINALIZADO = %s',
                (request.user.id, False))
            linha = cursor.fetchall()
            print("Linha aqui", linha)
        #print(linha, len(linha))
    return render(request, 'index.html', {'primario':pri, 'produtos':produtos, 'pedidos':pedidos, 'carrinho':carrinho, 'prod':linha})

def cadastro(request):
    form = UserModelForm(request.POST or None)
    bairros = Bairro.objects.all()
    if request.method == 'POST':
        if form.is_valid():
            form.save()
            return redirect('contas/login')
        else:
            print('eqiw')
    return render(request, 'cadastro.html', {'bairro':bairros})

def pedidos(request):
    #pedidos = Pedido.objects.filter(cod_cliente=request.user.id)
    pedidos = Pedido.objects.filter(cod_cliente=request.user.id)
    produtos = ProdutoPedido.objects.filter(cod_pedido__cod_cliente=request.user.id)
    with connection.cursor() as cursor:
        cursor.execute(
            'SELECT COD_COMPRA, SUM(VALOR) FROM CORE_PRODUTOPEDIDO INNER JOIN CORE_PRODUTO ON COD_PROD_ID = COD_ING INNER JOIN CORE_PEDIDO ON COD_PEDIDO_ID = COD_COMPRA INNER JOIN CORE_USUARIO ON COD_CLIENTE_ID = ID WHERE CORE_USUARIO.ID = %s GROUP BY COD_COMPRA',
            (request.user.id,))
        total = cursor.fetchall()
        print(total)
    return render(request, 'pedidos.html', {'pedidos':pedidos, 'produtos':produtos, 'total':total})

def finalizar(request, pk):
    #produto = get_object_or_404(ProdutoPedido, pk=pedidos.cod_pedido.cod_compra)
    #produto.delete()
    #return redirect()
    forma = FormaPagamento.objects.all()
    form = PagamentoModelForm(request.POST or None)
    bairro = Usuario.objects.get(id=request.user.id)
    taxa = Bairro.objects.get(nome=bairro.bairro)
    carrinho = ProdutoPedido.objects.filter(cod_pedido__finalizado=False, cod_pedido__cod_cliente=request.user.id)
    p = ProdutoPedido.objects.filter(cod_prod__cod_ing=pk, cod_pedido__cod_cliente=request.user.id, cod_pedido__finalizado=False)
    #print("Aqui MLK", p)
    p.delete()
    #print(p)
    #return redirect('index')
    with connection.cursor() as cursor:
        cursor.execute('SELECT COD_COMPRA, NOME FROM CORE_PRODUTOPEDIDO INNER JOIN CORE_PRODUTO ON COD_PROD_ID = COD_ING INNER JOIN CORE_PEDIDO ON COD_PEDIDO_ID = COD_COMPRA INNER JOIN CORE_USUARIO ON COD_CLIENTE_ID = ID WHERE CORE_USUARIO.ID = %s AND FINALIZADO = %s', (request.user.id, False))
        linha = cursor.fetchall()
    if form.is_valid():
        with connection.cursor() as cursor:
            cursor.execute('SELECT COD_COMPRA, SUM(TOTAL) FROM CORE_PRODUTOPEDIDO INNER JOIN CORE_PRODUTO ON COD_PROD_ID = COD_ING INNER JOIN CORE_PEDIDO ON COD_PEDIDO_ID = COD_COMPRA INNER JOIN CORE_USUARIO ON COD_CLIENTE_ID = ID WHERE CORE_USUARIO.ID = %s AND COD_COMPRA = %s ORDER BY COD_COMPRA',
                           (request.user.id, linha[0][0]))
            total_valor = cursor.fetchall()
        form = FormaPagamento.objects.get(forma=form.cleaned_data['forma'])
        pedido = Pedido.objects.filter(controle=True).filter(cod_cliente=request.user.id).filter(status='Aguardando confirmação').update(cod_forma=form.cod_forma, finalizado=True)
        return redirect('index')
        #ped = Pedido.objects.filter(cod_cliente=request.user.id, controle=True, finalizado=False).update(finalizado=True)
        #with connection.cursor() as cursor:
           # cursor.execute('UPDATE CORE_PEDIDO SET COD_FORMA_ID = %s WHERE CONTROLE = %s AND COD_CLIENTE_ID = %s AND STATUS = %s', (form.cod_forma, True, request.user.id, 'Aguardando confirmação'))
    else:
        print("aqio")
    return render(request, 'finalizar.html', {'forma':forma, 'carrinho':carrinho, 'produtos':linha})

def taxas(request):
    taxas = Bairro.objects.all()
    return render(request, 'taxa.html', {'taxas':taxas})