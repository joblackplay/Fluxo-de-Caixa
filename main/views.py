from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required,permission_required
from django.db.models import Sum
from django.contrib import messages
from movimentacoes.models import  Entrada,Saida
from django.utils import timezone
import json
from datetime import timedelta
from metas.models import MetaMensal
from django.contrib.auth.decorators import login_required, permission_required, user_passes_test
from django.core.exceptions import PermissionDenied
#from accounts.models import Account



@login_required(login_url = 'login')
# @user_passes_test(Account.is_admin, login_url='entrada', redirect_field_name=None)
def home(request):
    hoje = timezone.now().date()
    primeiro_dia_mes = hoje.replace(day=1)

    # === Totais do Dia ===
    total_entradas_dia = Entrada.objects.filter(data=hoje).aggregate(Sum('valor'))['valor__sum'] or 0
    total_saidas_dia = Saida.objects.filter(data=hoje).aggregate(Sum('valor'))['valor__sum'] or 0
    saldo_dia = total_entradas_dia - total_saidas_dia

    # === Totais do Mês ===
    total_entradas_mes = Entrada.objects.filter(data__gte=primeiro_dia_mes).aggregate(Sum('valor'))['valor__sum'] or 0
    total_saidas_mes = Saida.objects.filter(data__gte=primeiro_dia_mes).aggregate(Sum('valor'))['valor__sum'] or 0
    saldo_mes = total_entradas_mes - total_saidas_mes

    # === Saldo Acumulado ===
    saldo_acumulado = (
        Entrada.objects.aggregate(Sum('valor'))['valor__sum'] or 0
    ) - (
        Saida.objects.aggregate(Sum('valor'))['valor__sum'] or 0
    )

    # === Meta Mensal ===
    meta_mensal = MetaMensal.get_meta_atual()
    meta_percent = min((saldo_mes / meta_mensal.valor_meta * 100), 100) if meta_mensal.valor_meta > 0 else 0
    faltante = meta_mensal.valor_meta - saldo_mes

    # Últimas movimentações
    ultimas_entradas = Entrada.objects.select_related('tipo').order_by('-data', '-hora')[:8]
    ultimas_saidas = Saida.objects.select_related('tipo').order_by('-data', '-hora')[:8]

    # === Gráficos - Últimos 7 dias ===
    dias = []
    entradas_7dias = []
    saidas_7dias = []

    for i in range(6, -1, -1):
        data = hoje - timedelta(days=i)
        dias.append(data.strftime('%a'))
        entr = Entrada.objects.filter(data=data).aggregate(Sum('valor'))['valor__sum'] or 0
        said = Saida.objects.filter(data=data).aggregate(Sum('valor'))['valor__sum'] or 0
        entradas_7dias.append(float(entr))
        saidas_7dias.append(float(said))

    # Distribuição de Saídas por Tipo
    tipos_saida = Saida.objects.values('tipo__nome').annotate(total=Sum('valor')).order_by('-total')
    tipos_labels = [item['tipo__nome'] for item in tipos_saida]
    tipos_values = [float(item['total']) for item in tipos_saida]

    context = {
        'total_entradas_dia': total_entradas_dia,
        'total_saidas_dia': total_saidas_dia,
        'saldo_dia': saldo_dia,
        
        'total_entradas_mes': total_entradas_mes,
        'total_saidas_mes': total_saidas_mes,
        'saldo_mes': saldo_mes,
        
        'saldo_acumulado': saldo_acumulado,
        
        # Meta Mensal
        'meta_mensal': meta_mensal,
        'meta_percent': meta_percent,
        'faltante': faltante,
        
        'entradas': ultimas_entradas,
        'saidas': ultimas_saidas,

        # Gráficos
        'dias': json.dumps(dias),
        'entradas_7dias': json.dumps(entradas_7dias),
        'saidas_7dias': json.dumps(saidas_7dias),
        'tipos_saida_labels': json.dumps(tipos_labels),
        'tipos_saida_values': json.dumps(tipos_values),
    }
    return render(request, 'home.html', context)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request,username=username,password=password)
        print(user)
        if user is not None:
            login(request,user)
            
            return redirect('home')
        else:
            messages.success(request,"Ocorreu um erro ao efetuar o login. Por favor, tente novamente.")
            return redirect('login')
    else:    
        return render(request,'login.html')
    
def logout_view(request):
    logout(request)
    messages.success(request, 'Você saiu do sistema.')
    return redirect('login')
