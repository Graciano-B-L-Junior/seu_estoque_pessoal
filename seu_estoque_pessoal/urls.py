from django.urls import path
from . import views

urlpatterns = [
    path('',views.Login,name="login"),
    path('cadastro',views.Cadastro,name="register"),
    path('recuperar-conta',views.RecuperarConta,name="retrieve-account"),
    path('estoque-geral',views.EstoqueGeral,name="general_inventory"),
    path('adicionar-produto',views.CadastroProduto,name='add_product'),
    path('estoque-categoria',views.EstoqueCategoria,name='category_inventory'),
    path('lista-estoque-categoria',views.ListarEstoqueCategoria,name='category_product_list'),
    path('lista-estoque-categoria/<str:nome_categoria>',views.ListarEstoqueCategoria,name='category_product_list'),
    path('estoque-fornecedor',views.EstoqueFornecedor,name='category_supplier'),
    path('lista-estoque-fornecedor',views.ListarEstoqueFornecedor,name='supplier_product_list'),
    path('lista-estoque-fornecedor/<str:nome_fornecedor>',views.ListarEstoqueFornecedor,name='supplier_product_list'),
    path('adicionar-fornecedor',views.AdicionarFornecedor,name='add_supplier'),
    path('adicionar-categoria',views.AdicionarCategoria,name='add_category'),
    path('editar-produto/<int:id>/<str:produto>',views.EditarProduto,name='edit_product'),
    path('logout',views.Logout,name='logout')
]
