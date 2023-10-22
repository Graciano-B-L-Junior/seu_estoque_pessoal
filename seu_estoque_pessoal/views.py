from django.shortcuts import render
from django.http import HttpResponse
from .forms import ProductForm
from . import models
# Create your views here.
def index(request):
    return render(request,'seu_estoque_pessoal/estoque-geral.html')

def CadastroProduto(request):
    
    if request.method == "GET":
        form = ProductForm()
        categorias = models.Categoria.objects.all()
        fornecedores = models.Fornecedor.objects.all()
        #form.categoria.choices = ((categoria.nome,categoria.nome) for categoria in categorias)
        #form.fornecedor.choices =((fornecedor.nome,fornecedor.nome) for fornecedor in fornecedores)
        return render(request,'seu_estoque_pessoal/cadastro-produto.html',{
            "form":form
        })