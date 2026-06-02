from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from cliente.models import Cliente
from animal.models import Animal
from servico.models import Servico
from agendamento.models import Agendamento
import json

# ==================== 1. READ (Listar Informações) ====================
def listar_dados(request, tabela):
    try:
        if tabela == 'clientes':
            dados = []
            for c in Cliente.objects.all():
                dados.append({
                    'id': c.id_cliente,
                    'nome': c.nome_completo,
                    'cpf': c.cpf_cliente,
                    'telefone': c.telefone_cliente,
                    'email': c.email_cliente,
                    'endereco': c.endereco_cliente
                })
                
        elif tabela == 'pets':
            dados = []
            for pet in Animal.objects.all():
                dados.append({
                    'id': pet.id_animal,
                    'nome_pet': pet.nome_pet,
                    'especie': pet.especie,
                    'raca': pet.raca,
                    'data_nascimento': pet.data_nascimento.strftime('%d/%m/%Y') if pet.data_nascimento else '',
                    'peso': pet.peso,
                    'dono': pet.cliente.nome_completo,
                    'observacoes': pet.observacoes
                })
                
        elif tabela == 'servicos':
            dados = []
            for s in Servico.objects.all():
                dados.append({
                    'id': s.id_servico,
                    'nome_servico': s.nome_servico,
                    'descricao': s.descricao_servico,
                    'preco': s.preco_servico,
                    'duracao': s.duracao_servico
                })
                
        elif tabela == 'agendamentos':
            dados = []
            for ag in Agendamento.objects.all():
                # Captura os serviços associados ao ManyToMany
                lista_servicos = ", ".join([s.nome_servico for s in ag.servicos.all()])
                dados.append({
                    'id': ag.id_agendamento,
                    'animal': ag.animal.nome_pet,
                    'dono': ag.animal.cliente.nome_completo,
                    'data': ag.data.strftime('%d/%m/%Y'),
                    'hora': ag.hora.strftime('%H:%M'),
                    'servicos': lista_servicos,
                    'valor_total': ag.valor_total,
                    'status': ag.status
                })
        else:
            return JsonResponse({'status': 'erro', 'message': 'Tabela não encontrada'}, status=404)
            
        return JsonResponse(dados, safe=False)
    except Exception as e:
        return JsonResponse({'status': 'erro', 'message': str(e)}, status=500)


# ==================== 2. CREATE (Cadastrar Informações) ====================
@csrf_exempt
def cadastrar_dado(request, tabela):
    if request.method != 'POST':
        return JsonResponse({'status': 'erro', 'message': 'Método não permitido'}, status=405)
        
    try:
        data = json.loads(request.body)
        
        if tabela == 'clientes':
            Cliente.objects.create(
                nome_completo=data['nome_completo'],
                cpf_cliente=data.get('cpf_cliente', ''),
                telefone_cliente=data['telefone_cliente'],
                endereco_cliente=data['endereco_cliente'],
                email_cliente=data['email_cliente']
            )
            
        elif tabela == 'pets':
            cliente_instancia = Cliente.objects.get(id_cliente=data['cliente_id'])
            Animal.objects.create(
                nome_pet=data['nome_pet'],
                especie=data['especie'],
                raca=data['raca'],
                data_nascimento=data['data_nascimento'], # Formato esperado: YYYY-MM-DD
                peso=float(data['peso']),
                observacoes=data.get('observacoes', ''),
                cliente=cliente_instancia
            )
            
        elif tabela == 'servicos':
            Servico.objects.create(
                nome_servico=data['nome_servico'],
                descricao_servico=data['descricao_servico'],
                preco_servico=float(data['preco_servico']),
                duracao_servico=int(data['duracao_servico'])
            )
            
        else:
            return JsonResponse({'status': 'erro', 'message': 'Tabela inválida para cadastro via painel'}, status=400)
            
        return JsonResponse({'status': 'sucesso', 'message': 'Registro salvo com sucesso no MySQL!'})
    except Exception as e:
        return JsonResponse({'status': 'erro', 'message': f'Erro ao salvar: {str(e)}'}, status=400)


# ==================== 3. DELETE (Excluir Informações) ====================
@csrf_exempt
def excluir_dado(request, tabela, id_registro):
    if request.method != 'DELETE':
        return JsonResponse({'status': 'erro', 'message': 'Método não permitido'}, status=405)
        
    try:
        if tabela == 'clientes':
            Cliente.objects.filter(id_cliente=id_registro).delete()
        elif tabela == 'pets':
            Animal.objects.filter(id_animal=id_registro).delete()
        elif tabela == 'servicos':
            Servico.objects.filter(id_servico=id_registro).delete()
        elif tabela == 'agendamentos':
            Agendamento.objects.filter(id_agendamento=id_registro).delete()
        else:
            return JsonResponse({'status': 'erro', 'message': 'Tabela não mapeada'}, status=400)
            
        return JsonResponse({'status': 'sucesso', 'message': 'Registro removido com sucesso!'})
    except Exception as e:
        return JsonResponse({'status': 'erro', 'message': f'Erro ao deletar: {str(e)}'}, status=400)