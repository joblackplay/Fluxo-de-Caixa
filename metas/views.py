from django.shortcuts import render,redirect
from django.contrib import messages
from .models import MetaMensal
from datetime import datetime,timedelta
from movimentacoes.models import Entrada,Saida
from django.contrib.auth.decorators import login_required,permission_required,user_passes_test
from django.db.models import Sum
from django.utils import timezone
from accounts.models import Account

# Create your views here.

@login_required
# @permission_required('metas.salvar_meta_mensal', raise_exception=True)
# @user_passes_test(Account.is_gerente_or_admin, login_url='dashboard', redirect_field_name=None)
def salvar_meta_mensal(request):
    if request.method == 'POST':
        mes_str = request.POST.get('mes')  # formato YYYY-MM
        valor = request.POST.get('valor_meta')
        
        try:
            mes = datetime.strptime(mes_str, '%Y-%m').date().replace(day=1)
            meta, created = MetaMensal.objects.update_or_create(
                mes=mes,
                defaults={'valor_meta': valor}
            )
            messages.success(request, f'Meta de {mes.strftime("%m/%Y")} atualizada para R$ {valor}!')
        except:
            messages.error(request, 'Erro ao salvar meta. Verifique os dados.')
    
    return redirect('home')


@login_required
# @permission_required('metas.salvar_meta_mensal', raise_exception=True)
# @user_passes_test(Account.is_gerente_or_admin, login_url='dashboard', redirect_field_name=None)
def historico_metas(request):
    ano_selecionado = request.GET.get('ano')
    hoje = timezone.now().date()
    ano_atual = hoje.year

    # Se não informou ano, usa o ano atual
    if not ano_selecionado:
        ano_selecionado = str(ano_atual)

    # Todas as metas do ano selecionado
    metas = MetaMensal.objects.filter(mes__year=ano_selecionado).order_by('mes')

    # Lista de anos disponíveis (últimos 5 anos + atual)
    anos_disponiveis = list(range(ano_atual - 4, ano_atual + 1))

    # Preparando dados para o gráfico de evolução
    historico = []
    meses = []
    metas_values = []
    realizados_values = []

    for meta in metas:
        primeiro_dia = meta.mes
        ultimo_dia = (meta.mes + timedelta(days=32)).replace(day=1) - timedelta(days=1)

        realizado = Entrada.objects.filter(
            data__gte=primeiro_dia, data__lte=ultimo_dia
        ).aggregate(Sum('valor'))['valor__sum'] or 0

        realizado -= Saida.objects.filter(
            data__gte=primeiro_dia, data__lte=ultimo_dia
        ).aggregate(Sum('valor'))['valor__sum'] or 0

        percentual = (realizado / meta.valor_meta * 100) if meta.valor_meta > 0 else 0

        status = 'success' if percentual >= 100 else 'warning' if percentual >= 70 else 'danger'

        historico.append({
            'meta': meta,
            'realizado': realizado,
            'percentual': percentual,
            'status': status
        })

        # Dados para o gráfico
        meses.append(meta.mes.strftime('%b/%Y'))
        metas_values.append(float(meta.valor_meta))
        realizados_values.append(float(realizado))

    context = {
        'historico': historico,
        'anos_disponiveis': anos_disponiveis,
        'ano_selecionado': ano_selecionado,
        'meses': meses,
        'metas_values': metas_values,
        'realizados_values': realizados_values,
    }

    return render(request, 'metas/historico_metas.html',context)
