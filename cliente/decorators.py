from django.contrib.auth.decorators import user_passes_test
from django.shortcuts import redirect
from django.contrib import messages

def staff_required(view_func):
    """
    Decorator que permite o acesso apenas para usuários com perfil Staff (Admin/Vet).
    Se for um cliente comum, redireciona para a dashboard dele com um alerta.
    """
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_staff:
            return view_func(request, *args, **kwargs)
        
        messages.error(request, 'Acesso negado! Você não tem permissão para acessar esta área.')
        return redirect('cliente:dashboard_cliente')
        
    return _wrapped_view