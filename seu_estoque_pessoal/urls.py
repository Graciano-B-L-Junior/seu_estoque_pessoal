from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name="general_inventory"),
    path('adicionar-produto',views.CadastroProduto,name='add_product')
]
