from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import Fornecedor
from .forms import FornecedorForm
from movimentacoes.models import Saida
from django.db.models import Sum


@login_required
def lista_fornecedores(request):
    
    fornecedores = Fornecedor.objects.filter(ativo=True).order_by('nome')
    #form = FornecedorForm()                     # ← Adicione esta linha
    return render(request, 'fornecedores/lista_fornecedores.html', {
        'fornecedores': fornecedores,
        #'form': form                            # ← Passe o form
    })


@login_required
def cadastrar_fornecedor(request):
    if request.method == 'POST':
        form = FornecedorForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Fornecedor cadastrado com sucesso!')
            return redirect('lista_fornecedores')
    else:
        form = FornecedorForm()
    
    return render(request, 'fornecedores/cadastrar_fornecedor.html', {'form': form})


@login_required
def editar_fornecedor(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    
    if request.method == 'POST':
        form = FornecedorForm(request.POST, instance=fornecedor)
        if form.is_valid():
            form.save()
            messages.success(request, f'Fornecedor "{fornecedor.nome}" atualizado com sucesso!')
            return redirect('lista_fornecedores')
        else:
            messages.error(request, 'Por favor, corrija os erros abaixo.')
    else:
        form = FornecedorForm(instance=fornecedor)
    
    return render(request, 'fornecedores/editar_fornecedor.html', {
        'form': form,
        'fornecedor': fornecedor
    })

@login_required
def deletar_fornecedor(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    
    if request.method == 'POST':
        nome_fornecedor = fornecedor.nome
        fornecedor.delete()
        messages.success(request, f'Fornecedor "{nome_fornecedor}" excluído com sucesso!')
        return redirect('lista_fornecedores')
    
    # Se alguém acessar via GET, redireciona de volta
    return redirect('lista_fornecedores')


@login_required
def fornecedor_detail(request, pk):
    fornecedor = get_object_or_404(Fornecedor, pk=pk)
    
    # Saídas relacionadas a este fornecedor
    saidas = Saida.objects.filter(fornecedor=fornecedor).select_related('tipo', 'produto').order_by('-data', '-hora')
    
    # Totais
    total_compras = saidas.aggregate(Sum('valor'))['valor__sum'] or 0
    total_saidas = saidas.count()
    
    # Últimas 10 movimentações
    ultimas_saidas = saidas[:10]
    
    context = {
        'fornecedor': fornecedor,
        'saidas': saidas,
        'ultimas_saidas': ultimas_saidas,
        'total_compras': total_compras,
        'total_saidas': total_saidas,
    }
    return render(request, 'fornecedores/fornecedor_detail.html', context)