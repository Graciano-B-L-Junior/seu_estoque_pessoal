from django import forms
from . import models


class LoginForm(forms.Form):
    email = forms.EmailField(label="E-mail")
    senha = forms.CharField(widget=forms.PasswordInput,label="Senha")

class CadastroForm(forms.Form):
    nome = forms.CharField(label="Seu nome")
    email = forms.EmailField(label="E-mail")
    senha = forms.CharField(widget=forms.PasswordInput,label="Senha")

class RecuperarContaForm(forms.Form):
    email = forms.CharField(label="Seu e-mail")

class ProductForm(forms.Form):
    nome = forms.CharField(label="Nome produto",max_length=100)
    quantidade = forms.IntegerField(label="Quantidade em estoque")
    preco_custo = forms.FloatField(label="Preço de custo",initial=0.0)
    preco_venda = forms.FloatField(label="Preço de venda",initial=0.0)
    radio_button_categoria = forms.ChoiceField(label="",
                                                widget=forms.RadioSelect,
                                               choices=(("nova_categoria","nova categoria"),
                                                ("existente","Categoria existente")),
                                                initial="Categoria existente")
    categoria = forms.ModelChoiceField(label="Categorias",required=False,queryset=models.Categoria.objects.all(),empty_label=None)
    new_categoria = forms.CharField(label="Nova Categoria",required=False)
    radio_button_fornecedor = forms.ChoiceField(label="",
                                                widget=forms.RadioSelect,
                                               choices=(("Novo fornecedor","Novo fornecedor"),
                                                ("Fornecedor existente","Fornecedor existente")),
                                                initial="Fornecedor existente")
    fornecedor = forms.ModelChoiceField(label="Fornecedor",required=False,queryset=models.Fornecedor.objects.all(),empty_label=None)
    new_fornecedor = forms.CharField(label="Novo Fornecedor",required=False)

    def __init__(self,fornecedor,categoria,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["categoria"].queryset = categoria
        self.fields["fornecedor"].queryset = fornecedor

class EditProductForm(ProductForm):

    def __init__(self, fornecedor, categoria, *args, **kwargs):
        super().__init__(fornecedor, categoria, *args, **kwargs)


class SearchProductByCategory(forms.Form):
    categoria_nome = forms.ModelChoiceField(label="Selecione a categoria",empty_label=None,
                                            queryset=models.Categoria.objects.all())
    
    def __init__(self,categoria:models.Categoria  
                 ,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["categoria_nome"].queryset = categoria

class SearchProductBySupplier(forms.Form):
    fornecedor = forms.ModelChoiceField(label="Selecione o fornecedor",empty_label=None,
                                            queryset=models.Fornecedor.objects.all())

    def __init__(self,fornecedor:models.Fornecedor,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.fields["fornecedor"].queryset = fornecedor

class AddSupplier(forms.Form):
    fornecedor = forms.CharField(label="Nome do novo fornecedor",max_length=100)

class AddCategory(forms.Form):
    categoria = forms.CharField(label="Nome da nova categoria",max_length=100)
