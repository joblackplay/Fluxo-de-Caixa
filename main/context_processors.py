def user_role(request):
    """
    Adiciona variáveis de permissão e usuário em TODOS os templates.
    Isso evita erros de sintaxe e deixa o código mais limpo.
    """
    if request.user.is_authenticated:
        groups = list(request.user.groups.values_list('name', flat=True))
        
        return {
            'is_admin': 'Administrador' in groups,
            'is_gerente': 'Gerente' in groups,
            'is_usuario': 'Usuário' in groups,
            'user_groups': groups,
            'user': request.user,
            'user_full_name': request.user.get_full_name() or request.user.username,
        }
    else:
        return {
            'is_admin': False,
            'is_gerente': False,
            'is_usuario': False,
            'user_groups': [],
            'user': None,
            'user_full_name': 'Visitante',
        }