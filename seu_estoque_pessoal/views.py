from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request,'seu_estoque_pessoal/estoque-geral.html')

def t(request):
    return HttpResponse("teste")