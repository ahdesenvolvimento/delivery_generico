from django.urls import path
from .views import index,\
    cadastro, pedidos, finalizar,\
    taxas, deletar, produtos, tipos_produtos,\
    deletar_tipo, tipos_pagamento, deletar_forma, \
    deletar_produto, deletar_taxa
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

    #path('', include('core.urls')),
]