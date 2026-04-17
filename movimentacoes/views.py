from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
import json
from .models import Entrada, Saida, TipoEntrada, TipoSaida
from .forms import EntradaForm, SaidaForm

# === ENTRADAS ===
def entradas_list(request):
    entradas = Entrada.objects.all().order_by('-data', '-hora')
    form = EntradaForm()
    return render(request, 'fluxo/entradas.html', {'entradas': entradas, 'form': form})


@require_POST
@csrf_exempt
def entrada_create(request):
    form = EntradaForm(request.POST)
    if form.is_valid():
        entrada = form.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Entrada salva com sucesso!',
            'entrada': {
                'id': entrada.id,
                'data': entrada.data.strftime('%d/%m/%Y'),
                'hora': entrada.hora.strftime('%H:%M'),
                'tipo_nome': entrada.tipo.nome,
                'descricao': entrada.descricao,
                'pagamento': entrada.pagamento,
                'observacao': entrada.observacao,
                'valor': float(entrada.valor)
            }
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Erro ao validar os dados',
            'errors': form.errors
        }, status=400)


# ====================== SAÍDAS ======================
def saidas_list(request):
    saidas = Saida.objects.all().order_by('-data', '-hora')
    form = SaidaForm()
    return render(request, 'fluxo/saidas.html', {'saidas': saidas, 'form': form})


@require_POST
@csrf_exempt
def saida_create(request):
    form = SaidaForm(request.POST)
    if form.is_valid():
        saida = form.save()
        return JsonResponse({
            'status': 'success',
            'message': 'Saída salva com sucesso!',
            'saida': {
                'id': saida.id,
                'data': saida.data.strftime('%d/%m/%Y'),
                'hora': saida.hora.strftime('%H:%M'),
                'tipo_nome': saida.tipo.nome,
                'descricao': saida.descricao,
                'pagamento': saida.pagamento,
                'observacao': saida.observacao,
                'valor': float(saida.valor)
            }
        })
    else:
        return JsonResponse({
            'status': 'error',
            'message': 'Erro ao validar os dados',
            'errors': form.errors
        }, status=400)


# ====================== TIPOS (opcional por enquanto) ======================
def tipos_entrada(request):
    return render(request, 'fluxo/tipos_entrada.html')

def tipos_saida(request):
    return render(request, 'fluxo/tipos_saida.html')