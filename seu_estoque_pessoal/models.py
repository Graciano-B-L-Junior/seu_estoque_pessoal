from django.db import models

# Create your models here.
class User(models.Model):
    email = models.EmailField(unique=True)
    nome = models.CharField(max_length=255)
    senha = models.CharField(max_length=255)

class Fornecedor(models.Model):
    nome = models.CharField(max_length=255)
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome

class Categoria(models.Model):
    nome = models.CharField(max_length=255)
    user = models.ForeignKey(User,null=True,on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.nome

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    quantidade = models.IntegerField(default=0)
    preco_custo = models.FloatField(default=0)
    preco_venda = models.FloatField(default=0)
    cliente = models.ForeignKey(User,on_delete=models.CASCADE,blank=True,null=True)
    fornecedor = models.ForeignKey(Fornecedor,on_delete=models.CASCADE,blank=True,null=True)
    Categoria = models.ForeignKey(Categoria,on_delete=models.CASCADE,blank=True,null=True)
