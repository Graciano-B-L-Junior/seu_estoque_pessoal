from django.shortcuts import render,redirect
from django.urls import reverse
from .forms import ProductForm,SearchProductByCategory,SearchProductBySupplier,\
    AddSupplier,AddCategory,LoginForm,\
    RecuperarContaForm,CadastroForm,EditProductForm
from . import models
from django.contrib import messages
from django.core.paginator import Paginator
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
                models.Categoria(user=new_account,nome="Nenhum").save()
                models.Fornecedor(user=new_account,nome="Nenhum").save()
            except Exception as error:
                print(error)
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
        produtos = models.Produto.objects.filter(
            user=models.User.objects.get(pk=request.session.get("user_id"))
        ).order_by('id')
        paginator = Paginator(produtos,1)
        sem_produtos = True if len(paginator.object_list) == 0 else False
        infos_totais = {}
        pagina_atual = 1
        if request.GET.get("pagina") !=None:
            pagina_atual = request.GET.get("pagina")
        page = paginator.page(pagina_atual)
        proxima_pagina = None
        pagina_anterior = None

        if sem_produtos == False:
            if page.has_next():
                proxima_pagina=page.next_page_number()
            if page.has_previous():
                pagina_anterior = page.previous_page_number()
            quantidade = len(paginator.object_list)
            custo_total =0
            lucro_bruto =0
            for produto in paginator.object_list:
                custo_total += produto.quantidade * produto.preco_custo
                lucro_bruto += produto.quantidade * produto.preco_venda
            infos_totais["quantidade"]=quantidade
            infos_totais["custo_total"] = custo_total
            infos_totais["lucro_bruto"] = lucro_bruto
        return render(request,'seu_estoque_pessoal/estoque-geral.html',{
            "produtos":page,
            "sem_produtos":sem_produtos,
            "infos_totais":infos_totais,
            "pagina_total":len(page.object_list),
            "total_produtos":paginator.count,
            "anterior":page.has_previous(),
            "proximo":page.has_next(),
            "proxima_pagina":proxima_pagina,
            "pagina_anterior":pagina_anterior
        })
    else:
        return redirect(Login)

def CadastroProduto(request):
    if request.session.get("user_id")!=None:
        if request.method == "GET":
            categoria = models.Categoria.objects.filter(
                user=models.User.objects.get(pk=request.session.get("user_id"))
            )
            fornecedor = models.Fornecedor.objects.filter(
                user=models.User.objects.get(pk=request.session.get("user_id"))
            )
            form = ProductForm(fornecedor=fornecedor,categoria=categoria)            
            return render(request,'seu_estoque_pessoal/cadastro-produto.html',{
                "form":form
            })
        if request.method == "POST":
            categoria = models.Categoria.objects.filter(
                user=models.User.objects.get(pk=request.session.get("user_id"))
            )
            fornecedor = models.Fornecedor.objects.filter(
                user=models.User.objects.get(pk=request.session.get("user_id"))
            )
            form = ProductForm(fornecedor,categoria,request.POST) 
            if form.is_valid():
                nome_produto = form.cleaned_data["nome"]
                quantidade = form.cleaned_data["quantidade"]
                preco_custo = form.cleaned_data["preco_custo"]
                preco_venda = form.cleaned_data["preco_venda"]
                categoria_radio = form.cleaned_data["radio_button_categoria"]
                categoria:models.Categoria
                match categoria_radio:
                    case "existente":
                        _categoria = form.cleaned_data["categoria"]
                        categoria = models.Categoria.objects.get(nome=_categoria)
                        pass
                    case "nova_categoria":
                        _categoria = form.cleaned_data["new_categoria"]
                        categoria = models.Categoria(nome=_categoria)
                fornecedor_radio = form.cleaned_data["radio_button_fornecedor"]
                fornecedor:models.Fornecedor
                match fornecedor_radio:
                    case "Novo fornecedor":
                        _fornecedor= form.cleaned_data["new_fornecedor"]
                        fornecedor = models.Fornecedor(nome=_fornecedor)
                        pass
                    case "Fornecedor existente":
                        _fornecedor= form.cleaned_data["fornecedor"]
                        fornecedor = models.Fornecedor.objects.get(nome=_fornecedor)
                        pass
                usuario = models.User.objects.get(pk=request.session.get("user_id"))
                fornecedor.user=usuario
                categoria.user=usuario
                fornecedor.save()
                categoria.save()
                produto = models.Produto(
                    nome=nome_produto,
                    quantidade=quantidade,
                    preco_custo=preco_custo,
                    preco_venda=preco_venda,
                    user=usuario,
                    fornecedor=fornecedor,
                    categoria=categoria,
                )
                produto.save()
                messages.success(request,"Produto cadastrado com sucesso")
                return redirect(CadastroProduto)
            # print(nome_produto,quantidade,preco_custo,preco_venda,categoria_radio)
            # print("#"*50)
            return render(request,'seu_estoque_pessoal/cadastro-produto.html',{
                "form":form
            })

    else:
        return redirect(Login)

def EstoqueCategoria(request):
    if request.session.get("user_id")!=None:
        if request.method == "GET":
            categorias = models.Categoria.objects.filter(
                user=models.User.objects.get(pk=request.session.get("user_id"))
            )
            form = SearchProductByCategory(categoria=categorias)
            return render(request,'seu_estoque_pessoal/estoque-categoria.html',{
                "form":form,
            })
        elif request.method == "POST":
            categorias = models.Categoria.objects.filter(
                user=models.User.objects.get(pk=request.session.get("user_id"))
            )
            form = SearchProductByCategory(categorias,request.POST)
            if form.is_valid():
                categoria = form.cleaned_data["categoria_nome"]
                
                
                return redirect(reverse('category_product_list',args=[categoria]))
            else:
                messages.error(request, "Erro ao utilizar formulário, tente novamente")
                return render(request,'seu_estoque_pessoal/estoque-categoria.html',{
                "form":form,
            })
    else:
        return redirect(Login)

def EstoqueFornecedor(request):
    if request.session.get("user_id")!=None:
        if request.method == "GET":
            fornecedor = models.Fornecedor.objects.filter(
                user=models.User.objects.get(pk=request.session.get("user_id"))
            )
            form = SearchProductBySupplier(fornecedor)
            #categorias = models.Categoria.objects.all()
            #fornecedores = models.Fornecedor.objects.all()
            #form.categoria.choices = ((categoria.nome,categoria.nome) for categoria in categorias)
            #form.fornecedor.choices =((fornecedor.nome,fornecedor.nome) for fornecedor in fornecedores)
            return render(request,'seu_estoque_pessoal/estoque-fornecedor.html',{
                "form":form,
            })
        elif request.method == "POST":
            fornecedor = models.Fornecedor.objects.filter(
                user=models.User.objects.get(pk=request.session.get("user_id"))
            )
            form = SearchProductBySupplier(fornecedor,request.POST)
            # IMPLEMENTAR SISTEMA DE QUERY DE PRODUTOS
            if form.is_valid():
                fornecedor = form.cleaned_data["fornecedor"]
                return redirect(reverse('supplier_product_list',args=[fornecedor]))
            else:
                messages.error(request, "Erro ao utilizar formulário, tente novamente")
                return render(request,'seu_estoque_pessoal/estoque-fornecedor.html',{
                "form":form,
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
                user = models.User.objects.get(pk=request.session.get("user_id"))
                nome = form.cleaned_data["fornecedor"]
                models.Fornecedor(user=user,nome=nome).save()
                messages.success(request,"Fornecedor adicionado com sucesso")
                return redirect(AdicionarFornecedor)
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
                user = models.User.objects.get(pk=request.session.get("user_id"))
                nome = form.cleaned_data["categoria"]
                models.Categoria(user=user,nome=nome).save()
                messages.success(request,"Fornecedor adicionado com sucesso")
                return redirect(AdicionarCategoria)
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

def EditarProduto(request,id,produto):
    if request.session.get("user_id")!=None:
        if request.method == "GET":
            user = models.User.objects.get(pk=request.session.get("user_id"))
            fornecedor = models.Fornecedor.objects.filter(
                user=user
            )
            categoria = models.Categoria.objects.filter(
                user=user
            )
            product = models.Produto.objects.get(
                pk=id,
                nome=produto
            )
            form = EditProductForm(fornecedor,categoria,initial={'categoria':product.categoria.pk,
                                                                 'fornecedor':product.fornecedor.pk,
                                                                 'nome':product.nome,
                                                                 'quantidade':product.quantidade,
                                                                 'preco_custo':product.preco_custo,
                                                                 'preco_venda':product.preco_venda})
            return render(request,'seu_estoque_pessoal/editar-produto.html',{
                "form":form
            })
        elif request.method == "POST":
            user = models.User.objects.get(pk=request.session.get("user_id"))
            fornecedor = models.Fornecedor.objects.filter(
                user=user
            )
            categoria = models.Categoria.objects.filter(
                user=user
            )
            product = models.Produto.objects.get(
                pk=id,
                nome=produto
            )
            form = EditProductForm(fornecedor,categoria,request.POST)
            if form.is_valid():
                nome_produto = form.cleaned_data["nome"]
                quantidade = form.cleaned_data["quantidade"]
                preco_custo = form.cleaned_data["preco_custo"]
                preco_venda = form.cleaned_data["preco_venda"]
                categoria_radio = form.cleaned_data["radio_button_categoria"]
                categoria:models.Categoria
                match categoria_radio:
                    case "existente":
                        _categoria = form.cleaned_data["categoria"]
                        categoria = models.Categoria.objects.get(nome=_categoria)
                        pass
                    case "nova_categoria":
                        _categoria = form.cleaned_data["new_categoria"]
                        categoria = models.Categoria(nome=_categoria)
                fornecedor_radio = form.cleaned_data["radio_button_fornecedor"]
                fornecedor:models.Fornecedor
                match fornecedor_radio:
                    case "Novo fornecedor":
                        _fornecedor= form.cleaned_data["new_fornecedor"]
                        fornecedor = models.Fornecedor(nome=_fornecedor)
                        pass
                    case "Fornecedor existente":
                        _fornecedor= form.cleaned_data["fornecedor"]
                        fornecedor = models.Fornecedor.objects.get(nome=_fornecedor)
                        pass
                usuario = models.User.objects.get(pk=request.session.get("user_id"))
                fornecedor.user=usuario
                categoria.user=usuario
                fornecedor.save()
                categoria.save()
                product.categoria=categoria
                product.fornecedor=fornecedor
                product.nome = nome_produto
                product.preco_custo=preco_custo
                product.preco_venda=preco_venda
                product.quantidade=quantidade
                product.save()
                messages.success(request,"Produto Editado com sucesso")
                return render(request,'seu_estoque_pessoal/editar-produto.html',{
                "form":form
                })
            else:
                messages.error(request,"Erro ao salvar dados do formulário")
                return render(request,'seu_estoque_pessoal/editar-produto.html',{
                "form":form
            })
    else:
        return redirect(Login)
    
def ListarEstoqueCategoria(request,nome_categoria):
    if request.session.get("user_id")!=None:
        categoria = models.Categoria.objects.get(nome=nome_categoria,
                                                            user=models.User.objects.get(pk=request.session.get("user_id")))
        produtos = models.Produto.objects.filter(categoria=categoria,
                                                user=models.User.objects.get(pk=request.session.get("user_id")))\
                                                .order_by('id')
        sem_produtos = True if len(produtos) == 0 else False
        infos_totais = {}
        pagina_atual = 1
        paginator = Paginator(produtos,1)
        
        pagina_atual = request.GET.get("pagina") if request.GET.get("pagina") != None else 1
        page = paginator.page(pagina_atual)
        proxima_pagina = None
        pagina_anterior = None
        anterior = page.has_previous()
        proximo = page.has_next()
        if sem_produtos == False:
            if proximo:
                proxima_pagina=page.next_page_number()
            if anterior:
                pagina_anterior=page.previous_page_number()
            quantidade = len(produtos)
            custo_total =0
            lucro_bruto =0
            for produto in produtos:
                custo_total += produto.quantidade * produto.preco_custo
                lucro_bruto += produto.quantidade * produto.preco_venda
            infos_totais["quantidade"]=quantidade
            infos_totais["custo_total"] = custo_total
            infos_totais["lucro_bruto"] = lucro_bruto
        return render(request,'seu_estoque_pessoal/lista-produtos-categoria.html',{
            "nome_categoria":nome_categoria,
            "produtos":page,
            "sem_produtos":sem_produtos,
            "infos_totais":infos_totais,
            "pagina_total":len(page.object_list),
            "total_produtos":paginator.count,
            "anterior":page.has_previous(),
            "proximo":page.has_next(),
            "proxima_pagina":proxima_pagina,
            "pagina_anterior":pagina_anterior
        })
    else:
        return redirect(Login)
    
def ListarEstoqueFornecedor(request,nome_fornecedor):
    if request.session.get("user_id")!=None:
        fornecedor = models.Fornecedor.objects.get(nome=nome_fornecedor,
                                                            user=models.User.objects.get(pk=request.session.get("user_id")))
        produtos = models.Produto.objects.filter(fornecedor=fornecedor,
                                                user=models.User.objects.get(pk=request.session.get("user_id")))\
                                                .order_by('id')
        sem_produtos = True if len(produtos) == 0 else False
        infos_totais = {}
        pagina_atual = 1
        paginator = Paginator(produtos,1)
        
        pagina_atual = request.GET.get("pagina") if request.GET.get("pagina") != None else 1
        page = paginator.page(pagina_atual)
        proxima_pagina = None
        pagina_anterior = None
        anterior = page.has_previous()
        proximo = page.has_next()
        if sem_produtos == False:
            if proximo:
                proxima_pagina=page.next_page_number()
            if anterior:
                pagina_anterior=page.previous_page_number()
            quantidade = len(produtos)
            custo_total =0
            lucro_bruto =0
            for produto in produtos:
                custo_total += produto.quantidade * produto.preco_custo
                lucro_bruto += produto.quantidade * produto.preco_venda
            infos_totais["quantidade"]=quantidade
            infos_totais["custo_total"] = custo_total
            infos_totais["lucro_bruto"] = lucro_bruto
        return render(request,'seu_estoque_pessoal/lista-produtos-fornecedor.html',{
            "nome_fornecedor":nome_fornecedor,
            "produtos":page,
            "sem_produtos":sem_produtos,
            "infos_totais":infos_totais,
            "pagina_total":len(page.object_list),
            "total_produtos":paginator.count,
            "anterior":page.has_previous(),
            "proximo":page.has_next(),
            "proxima_pagina":proxima_pagina,
            "pagina_anterior":pagina_anterior
        })
    else:
        return redirect(Login)