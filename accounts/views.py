from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages 
from django.contrib.auth.decorators import login_required,permission_required,user_passes_test
from django.contrib.auth.forms import UserCreationForm
from .models import Account
from .forms import SignUpForm


@login_required
#@user_passes_test(Account.is_admin, login_url='lista_usuarios', redirect_field_name=None)
def register_view(request):
    # if request.user.is_authenticated:
    #     return redirect('login')
        
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Conta criada com sucesso! Bem-vindo!')
            return redirect('lista_usuarios')
        else:
            messages.error(request, 'Erro ao criar conta. Verifique os dados.')
    else:
        form = SignUpForm()
    
    return render(request, 'accounts/register.html', {'form': form})

@login_required
#@user_passes_test(Account.is_gerente_or_admin, login_url='lista_usuarios', redirect_field_name=None)
def lista_usuarios(request):
    usuarios = User.objects.all().order_by('-date_joined')
    groups = Group.objects.all()
    return render(request, 'accounts/lista_usuarios.html', {
        'usuarios': usuarios,
        'groups': groups
    })


@login_required
@user_passes_test(Account.is_admin, login_url='lista_usuarios', redirect_field_name=None)
def editar_role(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        novo_grupo_id = request.POST.get('group_id')
        if novo_grupo_id:
            # Remove todos os grupos atuais
            usuario.groups.clear()
            # Adiciona o novo grupo
            novo_grupo = Group.objects.get(id=novo_grupo_id)
            usuario.groups.add(novo_grupo)
            messages.success(request, f'Role de {usuario.username} alterada para {novo_grupo.name} com sucesso!')
        else:
            messages.error(request, 'Selecione um cargo.')
    
    return redirect('lista_usuarios')
