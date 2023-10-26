from django.urls import path
from . import views

urlpatterns = [
    path('',views.Login,name="login"),
    path('cadastro',views.Cadastro,name="register"),
    path('recuperar-conta',views.RecuperarConta,name="retrieve-account"),
    path('estoque-geral',views.EstoqueGeral,name="general_inventory"),
    path('adicionar-produto',views.CadastroProduto,name='add_product'),
    path('estoque-categoria',views.EstoqueCategoria,name='category_inventory'),
    path('estoque-fornecedor',views.EstoqueFornecedor,name='category_supplier'),
    path('adicionar-fornecedor',views.AdicionarFornecedor,name='add_supplier'),
    path('adicionar-categoria',views.AdicionarCategoria,name='add_category'),
    path('logout',views.Logout,name='logout')
]
