from django import forms

class ProductForm(forms.Form):
    nome = forms.CharField(label="Nome produto",max_length=100)
    quantidade = forms.IntegerField(label="Quantidade em estoque")
    preco_custo = forms.FloatField(label="Preço de custo",initial=0.0)
    preco_venda = forms.FloatField(label="Preço de venda",initial=0.0)
    radio_button_categoria = forms.ChoiceField(label="",
                                                widget=forms.RadioSelect,
                                               choices=(("nova categoria","nova categoria"),
                                                ("Categoria existente","Categoria existente")),
                                                initial="Categoria existente")
    categoria = forms.ChoiceField(label="Categorias",required=False)
    new_categoria = forms.CharField(label="Nova Categoria",required=False)
    radio_button_fornecedor = forms.ChoiceField(label="",
                                                widget=forms.RadioSelect,
                                               choices=(("Novo fornecedor","Novo fornecedor"),
                                                ("Fornecedor existente","Fornecedor existente")),
                                                initial="Fornecedor existente")
    fornecedor = forms.ChoiceField(label="Fornecedor",required=False)
    new_fornecedor = forms.CharField(label="Novo Fornecedor",required=False)