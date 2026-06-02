from django.contrib.auth.decorators import login_required
from django.db.models import Sum
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages

from animal.models import Animal
from agendamento.models import Agendamento
from cliente.models import Cliente
from servico.models import Servico
from .decorators import staff_required  # Importa nosso novo decorator

# ==================== 🐶 PAINEL DO CLIENTE ====================
@login_required
def dashboard_cliente(request):
    """Painel exclusivo para o cliente gerenciar seus pets e agendamentos."""
    # Garante que administradores não fiquem presos na visão de cliente
    if request.user.is_staff:
        return redirect('cliente:dashboard_admin')

    cliente = get_object_or_404(Cliente, usuario=request.user)

    # Lógica de atualização de perfil embutida que fizemos anteriormente
    if request.method == 'POST' and request.POST.get('action') == 'atualizar_perfil':
        cliente.nome_completo = request.POST.get('nome_completo', '').strip()
        cliente.cpf_cliente = request.POST.get('cpf', '').strip()
        cliente.telefone_cliente = request.POST.get('telefone', '').strip()
        cliente.endereco_cliente = request.POST.get('endereco', '').strip()
        cliente.save()
        
        nomes = cliente.nome_completo.split(' ', 1)
        request.user.first_name = nomes[0]
        request.user.save()
        
        messages.success(request, 'Perfil atualizado com sucesso!')
        return redirect('cliente:dashboard_cliente')

    context = {
        'cliente': cliente,
        'meus_animais': Animal.objects.filter(cliente=cliente),
        'meus_agendamentos': Agendamento.objects.filter(animal__cliente=cliente).select_related('animal').order_by('-data')
    }
    return render(request, 'cliente/dashboard_cliente.html', context)


# ==================== 🛠️ PAINEL DO ADMINISTRADOR / VET ====================
@login_required
@staff_required  # <-- Proteção dupla: precisa estar logado E ser staff
def dashboard_admin(request):
    """Painel completo para funcionários gerenciarem o estabelecimento."""
    faturamento = Agendamento.objects.aggregate(total=Sum('valor_total'))['total'] or 0
    
    context = {
        'todos_animais': Animal.objects.all(),
        'todos_agendamentos': Agendamento.objects.select_related('animal', 'animal__cliente').all().order_by('-data'),
        'todos_clientes': Cliente.objects.all(),
        'todos_servicos': Servico.objects.all(),
        'faturamento': faturamento,
        'total_agendamentos': Agendamento.objects.count(),
        'total_animais': Animal.objects.count(),
        'total_clientes': Cliente.objects.count(),
    }
    return render(request, 'cliente/dashboard_admin.html', context)


# ==================== ⚡ AÇÃO ADMINISTRATIVA: ALTERAR STATUS ====================
@login_required
@staff_required
def alterar_status_agendamento(request, agendamento_id, novo_status):
    """Permite que o funcionário altere o status de um agendamento na fila."""
    agendamento = get_object_or_404(Agendamento, pk=agendamento_id)
    
    # Valida se o status enviado é um dos permitidos no modelo
    if novo_status in ['Agendado', 'Concluído', 'Cancelado']:
        agendamento.status = novo_status
        agendamento.save()
        messages.success(request, f'Status do agendamento de {agendamento.animal.nome_pet} alterado para {novo_status}!')
    else:
        messages.error(request, 'Status inválido.')
        
    return redirect('cliente:dashboard_admin')