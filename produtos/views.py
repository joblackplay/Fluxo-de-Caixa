from django.shortcuts import render,redirect,get_object_or_404
from .forms import ProdutoForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Produto

@login_required
def lista_produtos(request):
    produtos = Produto.objects.order_by('nome')
    return render(request, 'produtos/lista_produtos.html', {'produtos': produtos})


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
    
    return render(request, 'produtos/modal_cadast_produto.html', {'form': form})

@login_required
def editar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        form = ProdutoForm(request.POST, instance=produto)
        if form.is_valid():
            form.save()
            messages.success(request, 'Produto atualizado com sucesso!')
            return redirect('lista_produtos')
    else:
        form = ProdutoForm(instance=produto)
    return render(request, 'produtos/editar_produto.html', {'form': form, 'produto': produto})


@login_required
def deletar_produto(request, pk):
    produto = get_object_or_404(Produto, pk=pk)
    if request.method == 'POST':
        nome = produto.nome
        produto.delete()
        messages.success(request, f'Produto "{nome}" excluído com sucesso!')
        return redirect('lista_produtos')
    return redirect('lista_produtos')

