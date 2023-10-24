from django.shortcuts import render
from django.http import HttpResponse
from .forms import ProductForm,SearchProductByCategory,SearchProductBySupplier,AddSupplier,AddCategory,LoginForm
from . import models
from django.contrib import messages
# Create your views here.

def Login(request):
    if request.method == "GET":
        form = LoginForm()
        return render(request,'seu_estoque_pessoal/index.html',{
            "form":form
        })
    elif request.method == "POST":
        form = LoginForm(request.POST)
        


def EstoqueGeral(request):
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

def EstoqueCategoria(request):
    if request.method == "GET":
        form = SearchProductByCategory()
        #categorias = models.Categoria.objects.all()
        #fornecedores = models.Fornecedor.objects.all()
        #form.categoria.choices = ((categoria.nome,categoria.nome) for categoria in categorias)
        #form.fornecedor.choices =((fornecedor.nome,fornecedor.nome) for fornecedor in fornecedores)
        return render(request,'seu_estoque_pessoal/estoque-categoria.html',{
            "form":form,
            "query_search":False
        })
    elif request.method == "POST":
        form = SearchProductByCategory(request.POST)
        # IMPLEMENTAR SISTEMA DE QUERY DE PRODUTOS
        if form.is_valid():
            #categoria = form.cleaned_data["categoria_nome"]
            #categoria = models.Categoria.objects.get(nome=categoria)
            #produtos = models.Produto.objects.filter(Categoria=categoria)
            return render(request,'seu_estoque_pessoal/estoque-categoria.html',{
            "form":form,
            "query_search":True
        })
        else:
            messages.error(request, "Erro ao utilizar formulário, tente novamente")
            return render(request,'seu_estoque_pessoal/estoque-categoria.html',{
            "form":form,
            "query_search":False
        })

def EstoqueFornecedor(request):
    if request.method == "GET":
        form = SearchProductBySupplier()
        #categorias = models.Categoria.objects.all()
        #fornecedores = models.Fornecedor.objects.all()
        #form.categoria.choices = ((categoria.nome,categoria.nome) for categoria in categorias)
        #form.fornecedor.choices =((fornecedor.nome,fornecedor.nome) for fornecedor in fornecedores)
        return render(request,'seu_estoque_pessoal/estoque-categoria.html',{
            "form":form,
            "query_search":False
        })
    elif request.method == "POST":
        form = SearchProductBySupplier(request.POST)
        # IMPLEMENTAR SISTEMA DE QUERY DE PRODUTOS
        if form.is_valid():
            #categoria = form.cleaned_data["categoria_nome"]
            #categoria = models.Categoria.objects.get(nome=categoria)
            #produtos = models.Produto.objects.filter(Categoria=categoria)
            return render(request,'seu_estoque_pessoal/estoque-categoria.html',{
            "form":form,
            "query_search":True
        })
        else:
            messages.error(request, "Erro ao utilizar formulário, tente novamente")
            return render(request,'seu_estoque_pessoal/estoque-categoria.html',{
            "form":form,
            "query_search":False
        })

def AdicionarFornecedor(request):
    if request.method == "GET":
        form = AddSupplier()
        return render(request,'seu_estoque_pessoal/adicionar-fornecedor.html',{
            "form":form
        })
    elif request.method == "POST":
        form = AddSupplier(request.POST)
        if form.is_valid():
            messages.success(request,"Fornecedor adicionado com sucesso")
            return render(request,'seu_estoque_pessoal/adicionar-fornecedor.html',{
                "form":form
            })
        else:
            messages.error(request,"Corrija o formulário")
            return render(request,'seu_estoque_pessoal/adicionar-fornecedor.html',{
                "form":form
            })

def AdicionarCategoria(request):
    if request.method == "GET":
        form = AddCategory()
        return render(request,'seu_estoque_pessoal/cadastro-categoria.html',{
            "form":form
        })
    elif request.method == "POST":
        form = AddCategory(request.POST)
        if form.is_valid():
            print("oi")
            messages.success(request,"Fornecedor adicionado com sucesso")
            return render(request,'seu_estoque_pessoal/cadastro-categoria.html',{
                "form":form
            })
        else:
            messages.error(request,"Corrija o formulário")
            return render(request,'seu_estoque_pessoal/cadastro-categoria.html',{
                "form":form
            })
