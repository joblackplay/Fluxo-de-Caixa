from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from movimentacoes.models import  Entrada,Saida
from collections import defaultdict
import json
from django.utils import timezone
from datetime import timedelta

@login_required(login_url = 'login')
def home(request):
     # === Cálculos principais ===
    hoje = timezone.now().date()

    # Totais do dia
    total_entradas = Entrada.objects.filter(data=hoje).aggregate(Sum('valor'))['valor__sum'] or 0
    total_saidas = Saida.objects.filter(data=hoje).aggregate(Sum('valor'))['valor__sum'] or 0
    saldo_dia = total_entradas - total_saidas

    # Saldo acumulado (todo histórico)
    saldo_acumulado = (
        Entrada.objects.aggregate(Sum('valor'))['valor__sum'] or 0
    ) - (
        Saida.objects.aggregate(Sum('valor'))['valor__sum'] or 0
    )

    # Últimas movimentações (para exibir na tabela)
    ultimas_entradas = Entrada.objects.select_related('tipo').order_by('-data', '-hora')[:6]
    ultimas_saidas = Saida.objects.select_related('tipo').order_by('-data', '-hora')[:6]

    # === Dados para os Gráficos (Últimos 7 dias) ===
    dias = []
    entradas_7dias = []
    saidas_7dias = []

    for i in range(6, -1, -1):  # de 6 dias atrás até hoje
        data = hoje - timedelta(days=i)
        dias.append(data.strftime('%a'))  # Ex: Seg, Ter, Qua...

        # Entradas do dia
        entr = Entrada.objects.filter(data=data).aggregate(Sum('valor'))['valor__sum'] or 0
        # Saídas do dia
        said = Saida.objects.filter(data=data).aggregate(Sum('valor'))['valor__sum'] or 0

        entradas_7dias.append(float(entr))
        saidas_7dias.append(float(said))

    # === Distribuição de Saídas por Tipo ===
    tipos_saida = Saida.objects.values('tipo__nome').annotate(
        total=Sum('valor')
    ).order_by('-total')

    tipos_labels = [item['tipo__nome'] for item in tipos_saida]
    tipos_values = [float(item['total']) for item in tipos_saida]

    context = {
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'saldo_dia': saldo_dia,
        'saldo_acumulado': saldo_acumulado,
        
        'entradas': ultimas_entradas,
        'saidas': ultimas_saidas,

        # Dados para gráficos
        'dias': json.dumps(dias),
        'entradas_7dias': json.dumps(entradas_7dias),
        'saidas_7dias': json.dumps(saidas_7dias),
        'tipos_saida_labels': json.dumps(tipos_labels),
        'tipos_saida_values': json.dumps(tipos_values),
    }

    return render(request,'home.html',context)

def login_user(request):
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
    
def logout_user(request):
    logout(request)
    messages.success(request, "You Have Been Logged Out...")
    return redirect('home')
