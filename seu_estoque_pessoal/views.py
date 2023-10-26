from django.shortcuts import render,redirect
from django.http import HttpResponse
from .forms import ProductForm,SearchProductByCategory,SearchProductBySupplier,\
    AddSupplier,AddCategory,LoginForm,\
    RecuperarContaForm,CadastroForm
from . import models
from django.contrib import messages
import uuid
# Create your views here.

def Login(request):
    if request.method == "GET":
        if request.session.get("login_form_completed")!=None:
            del request.session["login_form_completed"]
            del request.session["user_id"]
        form = LoginForm()
        return render(request,'seu_estoque_pessoal/index.html',{
            "form":form
        })
    elif request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            email= form.cleaned_data["email"]
            passw = form.cleaned_data["senha"]
            try:
                user = models.User.objects.get(email=email,senha=passw)
                request.session["login_form_completed"]=True
                request.session["user_id"]=user.pk
                request.session.set_expiry(120 * 60)
                return redirect(EstoqueGeral)
            except:
                messages.error(request,"Login ou senha errados")
                return render(request,'seu_estoque_pessoal/index.html',{
                "form":form
                })
        else:
            messages.error(request,"Ocorreu um erro com o formulário, tente novamente")
            return render(request,'seu_estoque_pessoal/index.html',{
                "form":form
            })
        
def Cadastro(request):
    if request.method == "GET":
        form = CadastroForm()
        return render(request,'seu_estoque_pessoal/cadastro.html',{
            "form":form
        })
    
    elif request.method == "POST":
        form = CadastroForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["nome"]
            email = form.cleaned_data["email"]
            passw= form.cleaned_data["senha"]
            new_account = models.User(nome=name,email=email,senha=passw)
            try:
                new_account.save()
            except:
                messages.error(request, "Já existe uma conta com esse e-mail!")
                return render(request,'seu_estoque_pessoal/cadastro.html',{
                "form":form
            })
            messages.success(request, "Conta criada com sucesso")
            return redirect(Login)
        else:
            messages.error(request, "Preencha os dados corretamente")
            return render(request,'seu_estoque_pessoal/cadastro.html',{
                "form":form
            })


def RecuperarConta(request):
    if request.method == "GET":
        form = RecuperarContaForm()
        return render(request,'seu_estoque_pessoal/recuperar-conta.html',{
            "form":form
        })
    
    elif request.method == "POST":
        form = RecuperarContaForm(request.POST)
        return render(request,'seu_estoque_pessoal/recuperar-conta.html',{
            "form":form
        })


def EstoqueGeral(request):
    if request.session.get("user_id")!=None:
        return render(request,'seu_estoque_pessoal/estoque-geral.html')
    else:
        return redirect(Login)

def CadastroProduto(request):
    if request.session.get("user_id")!=None:
        if request.method == "GET":
            form = ProductForm()
            categorias = models.Categoria.objects.all()
            fornecedores = models.Fornecedor.objects.all()
            #form.categoria.choices = ((categoria.nome,categoria.nome) for categoria in categorias)
            #form.fornecedor.choices =((fornecedor.nome,fornecedor.nome) for fornecedor in fornecedores)
            return render(request,'seu_estoque_pessoal/cadastro-produto.html',{
                "form":form
            })
        if request.method == "POST":
            form = ProductForm(request.POST)
            if form.is_valid():
                nome_produto = form.cleaned_data["nome"]
                quantidade = form.cleaned_data["quantidade"]
                preco_custo = form.cleaned_data["preco_custo"]
                preco_venda = form.cleaned_data["preco_venda"]
                categoria_radio = form.cleaned_data["radio_button_categoria"]
                match categoria_radio:
                    case "Categoria exsitente":
                        pass
                    case "nova categoria":
                        pass
                fornecedor_radio = form.cleaned_data["radio_button_fornecedor"]
                match fornecedor_radio:
                    case "":
                        pass
                    case "":
                        pass
            print(nome_produto,quantidade,preco_custo,preco_venda,categoria_radio)
            print("#"*50)
            return render(request,'seu_estoque_pessoal/cadastro-produto.html',{
                "form":form
            })

    else:
        return redirect(Login)

def EstoqueCategoria(request):
    if request.session.get("user_id")!=None:
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
    else:
        return redirect(Login)

def EstoqueFornecedor(request):
    if request.session.get("user_id")!=None:
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
    else:
        return redirect(Login)

def AdicionarFornecedor(request):
    if request.session.get("user_id")!=None:
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
    else:
        return redirect(Login)

def AdicionarCategoria(request):
    if request.session.get("user_id")!=None:
        if request.method == "GET":
            form = AddCategory()
            return render(request,'seu_estoque_pessoal/cadastro-categoria.html',{
                "form":form
            })
        elif request.method == "POST":
            form = AddCategory(request.POST)
            if form.is_valid():
                messages.success(request,"Fornecedor adicionado com sucesso")
                return render(request,'seu_estoque_pessoal/cadastro-categoria.html',{
                    "form":form
                })
            else:
                messages.error(request,"Corrija o formulário")
                return render(request,'seu_estoque_pessoal/cadastro-categoria.html',{
                    "form":form
                })
    else:
        return redirect(Login)
    
def Logout(request):
    del request.session["login_form_completed"]
    del request.session["user_id"]
    return redirect(Login)
