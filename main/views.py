from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.contrib import messages
from movimentacoes.models import  Entrada,Saida
from django.utils import timezone


@login_required(login_url = 'login')
def home(request):
    hoje = timezone.now().date()

    total_entradas = Entrada.objects.filter(data=hoje).aggregate(Sum('valor'))['valor__sum'] or 0
    total_saidas = Saida.objects.filter(data=hoje).aggregate(Sum('valor'))['valor__sum'] or 0
    saldo_dia = total_entradas - total_saidas

    # Saldo Acumulado (todo o histórico)
    saldo_acumulado = (
        Entrada.objects.aggregate(Sum('valor'))['valor__sum'] or 0
    ) - (
        Saida.objects.aggregate(Sum('valor'))['valor__sum'] or 0
    )

    # Últimas movimentações
    ultimas_entradas = Entrada.objects.select_related('tipo').order_by('-data', '-hora')[:8]
    ultimas_saidas = Saida.objects.select_related('tipo').order_by('-data', '-hora')[:8]

    context = {
        'total_entradas': total_entradas,
        'total_saidas': total_saidas,
        'saldo_dia': saldo_dia,
        'saldo_acumulado': saldo_acumulado,
        'entradas': ultimas_entradas,
        'saidas': ultimas_saidas,
    }
    return render(request,'home.html',context)


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
