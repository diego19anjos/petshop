from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cliente.models import Cliente
from .models import Agendamento, AgendamentoServico
from .forms import AgendamentoForm

@login_required
def fazer_agendamento(request):
    """Gere a criação de um novo agendamento calculando o valor total dos serviços."""
    cliente = get_object_or_404(Cliente, usuario=request.user)

    if request.method == 'POST':
        # Passamos o cliente no kwargs para que o formulário saiba filtrar os pets
        form = AgendamentoForm(request.POST, cliente=cliente)
        
        if form.is_valid():
            # 1. Instancia o agendamento mas não salva no banco ainda (commit=False)
            agendamento = form.save(commit=False)
            agendamento.save() # Salva para gerar o ID_agendamento necessário para a tabela intermediária

            # 2. Captura os serviços selecionados no formulário
            servicos_selecionados = form.cleaned_data['servicos']
            
            valor_total = 0
            
            # 3. Loop para criar as relações na tabela ManyToMany (AgendamentoServico)
            for servico in servicos_selecionados:
                AgendamentoServico.objects.create(
                    agendamento=agendamento,
                    servico=servico
                )
                valor_total += servico.preco_servico # Soma o preço de cada um

            # 4. Atualiza o agendamento com o valor total calculado
            agendamento.valor_total = valor_total
            agendamento.save()

            messages.success(request, f'Agendamento para {agendamento.animal.nome_pet} realizado com sucesso! Total: R$ {valor_total:.2f}')
            return redirect('cliente:dashboard')
    else:
        form = AgendamentoForm(cliente=cliente)

    return render(request, 'agendamento/marcar.html', {'form': form})