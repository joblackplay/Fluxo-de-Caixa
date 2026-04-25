from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Produto, Fornecedor
from .forms import ProdutoForm



@login_required
def lista_produtos(request):
    produtos = Produto.objects.prefetch_related('fornecedores').order_by('nome')
    fornecedores = Fornecedor.objects.filter(ativo=True).order_by('nome')
    
    return render(request, 'produtos/lista_produtos.html', {
        'produtos': produtos,
        'fornecedores': fornecedores
    })

@login_required
def cadastrar_produto(request):
    if request.method == 'POST':
        form = ProdutoForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto cadastrado com sucesso!')
            return redirect('lista_produtos')
    else:
        form = ProdutoForm()
    
    fornecedores = Fornecedor.objects.filter(ativo=True)
    return render(request, 'fluxo/cadastrar_produto.html', {
        'form': form,
        'fornecedores': fornecedores
    })