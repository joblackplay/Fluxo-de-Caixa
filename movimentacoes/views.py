from django.shortcuts import render,redirect,get_object_or_404
from django.contrib import messages
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST,require_GET
from django.db.models import Sum
from .models import Entrada, Saida, TipoEntrada, TipoSaida
from .forms import EntradaForm, SaidaForm
from django.contrib.auth.decorators import login_required,user_passes_test
from django.utils import timezone



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

@login_required
def dre(request):
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')

    entradas = Entrada.objects.select_related('tipo')
    saidas = Saida.objects.select_related('tipo')

    if data_inicial:
        entradas = entradas.filter(data__gte=data_inicial)
        saidas = saidas.filter(data__gte=data_inicial)
    if data_final:
        entradas = entradas.filter(data__lte=data_final)
        saidas = saidas.filter(data__lte=data_final)

    # Dados para tabelas e gráficos
    entradas_por_tipo = list(entradas.values('tipo__nome').annotate(total=Sum('valor')).order_by('-total'))
    saidas_por_tipo = list(saidas.values('tipo__nome').annotate(total=Sum('valor')).order_by('-total'))

    total_entradas = sum(item['total'] for item in entradas_por_tipo)
    total_saidas = sum(item['total'] for item in saidas_por_tipo)
    resultado = total_entradas - total_saidas

    # Calcula percentuais
    for item in entradas_por_tipo:
        item['percentual'] = (item['total'] / total_entradas * 100) if total_entradas > 0 else 0
    for item in saidas_por_tipo:
        item['percentual'] = (item['total'] / total_saidas * 100) if total_saidas > 0 else 0

    # Dados para Gráfico de Barras Comparativo
    # Une os tipos mais importantes para comparação
    tipos = set([item['tipo__nome'] for item in entradas_por_tipo] + [item['tipo__nome'] for item in saidas_por_tipo])
    bar_labels = list(tipos)
    bar_entradas = []
    bar_saidas = []

    for tipo in bar_labels:
        entr = next((item['total'] for item in entradas_por_tipo if item['tipo__nome'] == tipo), 0)
        said = next((item['total'] for item in saidas_por_tipo if item['tipo__nome'] == tipo), 0)
        bar_entradas.append(float(entr))
        bar_saidas.append(float(said))

    context = {
        'entradas_por_tipo': entradas_por_tipo,
        'saidas_por_tipo': saidas_por_tipo,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'resultado': resultado,
        'data_inicial': data_inicial,
        'data_final': data_final,
        
        # Gráficos
        'entradas_labels': json.dumps([item['tipo__nome'] for item in entradas_por_tipo]),
        'entradas_values': json.dumps([float(item['total']) for item in entradas_por_tipo]),
        'saidas_labels': json.dumps([item['tipo__nome'] for item in saidas_por_tipo]),
        'saidas_values': json.dumps([float(item['total']) for item in saidas_por_tipo]),
        
        # Gráfico de Barras Comparativo
        'bar_labels': json.dumps(bar_labels),
        'bar_entradas': json.dumps(bar_entradas),
        'bar_saidas': json.dumps(bar_saidas),
    }
    return render(request, 'fluxo/dre.html', context)

@login_required
def fluxo_de_caixa(request):
    data_inicial = request.GET.get('data_inicial')
    data_final = request.GET.get('data_final')

    entradas = Entrada.objects.select_related('tipo')
    saidas = Saida.objects.select_related('tipo')

    if data_inicial:
        entradas = entradas.filter(data__gte=data_inicial)
        saidas = saidas.filter(data__gte=data_inicial)
    if data_final:
        entradas = entradas.filter(data__lte=data_final)
        saidas = saidas.filter(data__lte=data_final)

    # Obter datas únicas
    datas_entradas = list(entradas.values_list('data', flat=True).distinct())
    datas_saidas = list(saidas.values_list('data', flat=True).distinct())
    todas_datas = sorted(set(datas_entradas) | set(datas_saidas))

    fluxo = []
    saldo_acumulado = 0

    for dia in todas_datas:
        entr = Entrada.objects.filter(data=dia).aggregate(Sum('valor'))['valor__sum'] or 0
        said = Saida.objects.filter(data=dia).aggregate(Sum('valor'))['valor__sum'] or 0
        saldo_dia = entr - said
        saldo_acumulado += saldo_dia

        fluxo.append({
            'data': dia,
            'entradas': float(entr),
            'saidas': float(said),
            'saldo_dia': float(saldo_dia),
            'saldo_acumulado': float(saldo_acumulado)
        })

    total_entradas = sum(item['entradas'] for item in fluxo)
    total_saidas = sum(item['saidas'] for item in fluxo)
    saldo_final = saldo_acumulado

    # Preparar dados para o gráfico
    datas = [item['data'].strftime('%d/%m') for item in fluxo]
    saldos_acumulados = [item['saldo_acumulado'] for item in fluxo]

    context = {
        'fluxo': fluxo,
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'saldo_final': saldo_final,
        'data_inicial': data_inicial,
        'data_final': data_final,
        'datas': json.dumps(datas),
        'saldos_acumulados': json.dumps(saldos_acumulados),
    }
    return render(request, 'fluxo/fluxo_de_caixa.html', context)
