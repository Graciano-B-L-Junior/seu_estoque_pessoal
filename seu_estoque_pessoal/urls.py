from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="general_inventory"),
    path('adicionar-produto',views.CadastroProduto,name='add_product'),
    path('estoque-categoria',views.EstoqueCategoria,name='category_inventory'),
    path('estoque-fornecedor',views.EstoqueFornecedor,name='category_supplier'),
    path('adicionar-fornecedor',views.AdicionarCategoria,name='add_supplier'),
]
