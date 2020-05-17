from django.urls import path
from .views import index, cadastro, pedidos, finalizar, taxas
urlpatterns = [
    path('', index, name='index'),
    path('cadastro', cadastro, name='cadastro'),
    path('pedidos', pedidos, name='pedidos'),
    path('finalizar/<int:pk>', finalizar, name='finalizar'),
    path('taxas', taxas, name='taxas'),
    #path('', include('core.urls')),
]