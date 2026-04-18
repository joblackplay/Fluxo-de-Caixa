from django.shortcuts import render,redirect
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import Entrada, Saida, TipoEntrada, TipoSaida
from .forms import EntradaForm, SaidaForm

# === ENTRADAS ===
def entradas_list(request):
    entradas = Entrada.objects.select_related('tipo').order_by('-data', '-hora')
    form = EntradaForm()
    return render(request, 'fluxo/entradas.html', {
        'entradas': entradas,
        'form': form
    })


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


# ====================== SAÍDAS ======================
def saidas_list(request):
    saidas = Saida.objects.select_related('tipo').order_by('-data', '-hora')
    form = SaidaForm()
    return render(request, 'fluxo/saidas.html', {
        'saidas': saidas,
        'form': form
    })


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