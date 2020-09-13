from django.urls import path
from .views import index, \
    cadastro, pedidos, finalizar,\
    taxas, deletar, produtos, tipos_produtos,\
    deletar_tipo, tipos_pagamento, deletar_forma, \
    deletar_produto, deletar_taxa, deletar_produto_carrinho_index, \
    administracao, ingredientes, motoboy, atualiza_produto, \
    atualiza_bairro, adicionais#, atualiza_promocao, deletar_promocao, promocao
#
urlpatterns = [
    path('', index, name='index'),
    path('cadastro', cadastro, name='cadastro'),
    path('pedidos', pedidos, name='pedidos'),
    path('finalizar', finalizar, name='finalizar'),
    path('deletar/<int:pk>', deletar, name='deletar'),
    path('taxas', taxas, name='taxas'),
    path('produtos', produtos, name='produtos'),
    path('deletar_produto/<int:pk>', deletar_produto, name='deletar_produto'),
    path('tipos_produtos', tipos_produtos, name='tipos_produtos'),
    path('deletar_tipo/<int:pk>', deletar_tipo, name='deletar_tipo'),
    path('tipos_pagamento', tipos_pagamento, name='tipos_pagamento'),
    path('deletar_forma/<int:pk>', deletar_forma, name='deletar_forma'),
    path('deletar_taxa/<int:pk>', deletar_taxa, name='deletar_taxa'),
    path('deletar_produto_index/<int:pk>', deletar_produto_carrinho_index, name='deletar_produto_carrinho_index'),
    path('administracao', administracao, name='administracao'),
    path('ingredientes', ingredientes, name='ingredientes'),
    path('motoboy', motoboy, name='motoboy'),
    # path('promocao', promocao, name='promocao'),
    path('atualiza_produto/<int:pk>', atualiza_produto, name='atualiza_produto'),
    path('atualiza_bairro/<int:pk>', atualiza_bairro, name='atualiza_bairro'),
    path('adicionais', adicionais, name='adicionais'),
    # path('atualiza_promocao/<int:pk>', atualiza_promocao, name='atualiza_promocao'),
    # path('deletar_promocao/<int:pk>', deletar_promocao, name='deletar_promocao'),

]

'''
    path('cadastro', cadastro, name='cadastro'),
    path('pedidos', pedidos, name='pedidos'),
    path('finalizar', finalizar, name='finalizar'),
    path('deletar/<int:pk>', deletar, name='deletar'),
    path('taxas', taxas, name='taxas'),
    path('produtos', produtos, name='produtos'),
    path('deletar_produto/<int:pk>', deletar_produto, name='deletar_produto'),
    path('tipos_produtos', tipos_produtos, name='tipos_produtos'),
    path('deletar_tipo/<int:pk>', deletar_tipo, name='deletar_tipo'),
    path('tipos_pagamento', tipos_pagamento, name='tipos_pagamento'),
    path('deletar_forma/<int:pk>', deletar_forma, name='deletar_forma'),
    path('deletar_taxa/<int:pk>', deletar_taxa, name='deletar_taxa'),
    path('deletar_produto_index/<int:pk>', deletar_produto_carrinho_index, name='deletar_produto_carrinho_index'),
    path('administracao', administracao, name='administracao'),
    path('ingredientes', ingredientes, name='ingredientes'),
    path('motoboy', motoboy, name='motoboy'),
    #path('promocao', promocao, name='promocao'),
    path('atualiza_produto/<int:pk>', atualiza_produto, name='atualiza_produto'),
    path('atualiza_bairro/<int:pk>', atualiza_bairro, name='atualiza_bairro'),
    #path('atualiza_promocao/<int:pk>', atualiza_promocao, name='atualiza_promocao'),
   # path('deletar_promocao/<int:pk>', deletar_promocao, name='deletar_promocao'),
    '''
    #path('', include('core.urls')),