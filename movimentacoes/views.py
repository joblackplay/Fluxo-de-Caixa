from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST,require_GET
import json
from .models import Entrada, Saida, TipoEntrada, TipoSaida
from .forms import EntradaForm, SaidaForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# === ENTRADAS ===
@login_required
def entradas_list(request):
    hoje = timezone.now().date()
    entradas = Entrada.objects.select_related('tipo').order_by('-data', '-hora')
    
    # Filtros
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')
    tipo_id = request.GET.get('tipo')
    pagamento = request.GET.get('pagamento')

    if not data_inicial and not data_final:
        data_inicial = hoje
        data_final = hoje

    if data_inicial:
        entradas = entradas.filter(data__gte=data_inicial)
    if data_final:
        entradas = entradas.filter(data__lte=data_final)
    if tipo_id:
        entradas = entradas.filter(tipo_id=tipo_id)
    if pagamento:
        entradas = entradas.filter(pagamento=pagamento)

    form = EntradaForm()
    tipos = TipoEntrada.objects.all()

    context = {
        'entradas': entradas,
        'form': form,
        'tipos': tipos,
        'data_inicial': data_inicial,
        'data_final': data_final,
        'tipo_selecionado': tipo_id,
        'pagamento_selecionado': pagamento,
        'hoje': hoje,
    }
    return render(request, 'fluxo/entradas.html', context)

@login_required
def entrada_create(request):
    if request.method == 'POST':
        form = EntradaForm(request.POST)
        if form.is_valid():
            entrada = form.save()
            messages.success(request, f'Entrada de R$ {entrada.valor} cadastrada com sucesso!')
            return redirect('entradas_list')
        else:
            messages.error(request, 'Erro ao salvar entrada. Verifique os campos obrigatórios.')
            # Retorna para a mesma página mantendo os erros do formulário
            entradas = Entrada.objects.select_related('tipo').order_by('-data', '-hora')
            return render(request, 'fluxo/entradas.html', {
                'entradas': entradas,
                'form': form
            })
    
    return redirect('entradas_list')

# @require_GET
# @login_required
# def entrada_get(request, pk):
#     entrada = get_object_or_404(Entrada, pk=pk)
#     return JsonResponse({
#         'id': entrada.id,
#         'tipo': entrada.tipo.id,
#         'descricao': entrada.descricao,
#         'valor': float(entrada.valor),
#         'pagamento': entrada.pagamento,
#     })


@login_required
def entrada_edit(request, pk):
   
    entrada = get_object_or_404(Entrada, pk=pk)
    
    if request.method == 'POST':
        form = EntradaForm(request.POST, instance=entrada)
        if form.is_valid():
            form.save()
            messages.success(request, 'Entrada atualizada com sucesso!')
            return redirect('entradas_list')
        else:
            messages.error(request, 'Erro ao atualizar. Verifique os dados.')
    else:
        form = EntradaForm(instance=entrada)
    
    return render(request, 'fluxo/entrada_edit.html', {
        'form': form,
        'entrada': entrada
    })

@login_required
def entrada_delete(request, pk):
    entrada = get_object_or_404(Entrada, pk=pk)
    
    if request.method == 'POST':
        entrada.delete()
        messages.success(request, f'Entrada "{entrada.descricao}" excluída com sucesso!')
        return redirect('entradas_list')
    
    # GET - Mostra página de confirmação
    return render(request, 'fluxo/entrada_confirm_delete.html', {'entrada': entrada})
    
    # return render(request, 'fluxo/entrada_confirm_delete.html', {'entrada': entrada})


# ====================== SAÍDAS ======================
@login_required
def saidas_list(request):
    hoje = timezone.now().date()
    
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')
    tipo_id = request.GET.get('tipo')
    pagamento = request.GET.get('pagamento')

    saidas = Saida.objects.select_related('tipo').order_by('-data', '-hora')

    if not data_inicial and not data_final:
        data_inicial = hoje
        data_final = hoje

    if data_inicial:
        saidas = saidas.filter(data__gte=data_inicial)
    if data_final:
        saidas = saidas.filter(data__lte=data_final)
    if tipo_id:
        saidas = saidas.filter(tipo_id=tipo_id)
    if pagamento:
        saidas = saidas.filter(pagamento=pagamento)

    form = SaidaForm()
    tipos = TipoSaida.objects.all()

    context = {
        'saidas': saidas,
        'form': form,
        'tipos': tipos,
        'data_inicial': data_inicial,
        'data_final': data_final,
        'tipo_selecionado': tipo_id,
        'pagamento_selecionado': pagamento,
    }
    return render(request, 'fluxo/saidas.html', context)

@login_required
def saida_create(request):
    if request.method == 'POST':
        form = SaidaForm(request.POST)
        if form.is_valid():
            saida = form.save()
            messages.success(request, f'Saída de R$ {saida.valor} cadastrada com sucesso!')
            return redirect('saidas_list')
        else:
            messages.error(request, 'Erro ao salvar saída. Verifique os campos obrigatórios.')
            saidas = Saida.objects.select_related('tipo').order_by('-data', '-hora')
            return render(request, 'fluxo/saidas.html', {
                'saidas': saidas,
                'form': form
            })
    
    return redirect('saidas_list')

@login_required
def saida_delete(request, pk):
    saida = get_object_or_404(Saida, pk=pk)
    
    if request.method == 'POST':
        saida.delete()
        messages.success(request, f'Saída "{saida.descricao}" excluída com sucesso!')
        return redirect('saidas_list')
    
    # GET - Página de confirmação
    return render(request, 'fluxo/saida_confirm_delete.html', {'saida': saida})


@login_required
def saida_edit(request, pk):
    saida = get_object_or_404(Saida, pk=pk)
    
    if request.method == 'POST':
        form = SaidaForm(request.POST, instance=saida)
        if form.is_valid():
            form.save()
            messages.success(request, 'Saída atualizada com sucesso!')
            return redirect('saidas_list')
        else:
            messages.error(request, 'Erro ao atualizar saída. Verifique os dados.')
    else:
        form = SaidaForm(instance=saida)
    
    return render(request, 'fluxo/saida_edit.html', {
        'form': form,
        'saida': saida
    })


# # ====================== TIPOS ======================
# def tipos_entrada(request):
#     tipos = TipoEntrada.objects.all().order_by('nome')
#     form = TipoEntradaForm()
#     return render(request, 'fluxo/tipos_entrada.html', {
#         'tipos': tipos,
#         'form': form
#     })


# def tipo_entrada_create(request):
#     if request.method == 'POST':
#         form = TipoEntradaForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Tipo de Entrada cadastrado com sucesso!')
#             return redirect('tipos_entrada')
#         else:
#             messages.error(request, 'Erro ao cadastrar tipo. Verifique os dados.')
#     return redirect('tipos_entrada')


# def tipos_saida(request):
#     tipos = TipoSaida.objects.all().order_by('nome')
#     form = TipoSaidaForm()
#     return render(request, 'fluxo/tipos_saida.html', {
#         'tipos': tipos,
#         'form': form
#     })


# def tipo_saida_create(request):
#     if request.method == 'POST':
#         form = TipoSaidaForm(request.POST)
#         if form.is_valid():
#             form.save()
#             messages.success(request, 'Tipo de Saída cadastrado com sucesso!')
#             return redirect('tipos_saida')
#         else:
#             messages.error(request, 'Erro ao cadastrar tipo. Verifique os dados.')
#     return redirect('tipos_saida')