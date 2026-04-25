from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth.models import Group, User
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages 
from django.contrib.auth.decorators import login_required,permission_required,user_passes_test
from django.contrib.auth.forms import UserCreationForm
from .models import Account
from .forms import SignUpForm
from django.http import JsonResponse

def is_admin(user):
    return user.groups.filter(name='Administrador').exists()

@login_required
@user_passes_test(Account.is_admin, login_url='home', redirect_field_name=None)
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
#@permission_required('auth.view_user', raise_exception=True)
def get_usuario(request, user_id):
    try:
        usuario = User.objects.get(id=user_id)
        group = usuario.groups.first()
        
        data = {
            'id': usuario.id,
            'username': usuario.username,
            'email': usuario.email,
            'first_name': usuario.first_name,
            'last_name': usuario.last_name,
            'group_id': group.id if group else '',
            'is_active': usuario.is_active,
        }
        return JsonResponse(data)
    except User.DoesNotExist:
        return JsonResponse({'error': 'Usuário não encontrado'}, status=404)
    

@login_required
#@permission_required('auth.change_user', raise_exception=True)
def editar_usuario(request, user_id):
    usuario = get_object_or_404(User, id=user_id)
    
    if request.method == 'POST':
        usuario.email = request.POST.get('email', usuario.email)
        usuario.first_name = request.POST.get('first_name', usuario.first_name)
        usuario.last_name = request.POST.get('last_name', usuario.last_name)
        usuario.is_active = 'is_active' in request.POST
        
        # Atualizar Role
        group_id = request.POST.get('group')
        if group_id:
            usuario.groups.clear()
            novo_grupo = Group.objects.get(id=group_id)
            usuario.groups.add(novo_grupo)
        
        usuario.save()
        messages.success(request, f'Usuário "{usuario.username}" atualizado com sucesso!')
        return redirect('lista_usuarios')
    
    # GET - Mostra formulário
    current_group = usuario.groups.first()
    groups = Group.objects.all()
    
    return render(request, 'accounts/usuario_edit.html', {
        'usuario': usuario,
        'groups': groups,
        'current_group': current_group
    })


@login_required
#@user_passes_test(Account.is_admin, login_url='lista_usuarios', redirect_field_name=None)
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

@login_required
def deletar_usuario(request, user_id):
    
    usuario = get_object_or_404(User, id=user_id)
    
    if usuario == request.user:
        messages.error(request, "Você não pode excluir sua própria conta!")
        return redirect('lista_usuarios')
    
    if usuario.is_superuser:
        messages.error(request, "Não é permitido excluir um Superusuário!")
        return redirect('lista_usuarios')
    
    if request.method == 'POST':
        nome = usuario.get_full_name() or usuario.username
        usuario.delete()
        messages.success(request, f'Usuário "{nome}" foi excluído permanentemente!')
        return redirect('lista_usuarios')
    
    # Se chegar via GET (não deve acontecer com modal), redireciona
    return redirect('lista_usuarios')