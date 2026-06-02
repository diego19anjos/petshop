from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from cliente.models import Cliente
from .models import Animal
from .forms import AnimalForm

@login_required
def listar_pets(request):
    """Lista apenas os animais do usuário logado ou todos se for administrador."""
    if request.user.is_staff:
        pets = Animal.objects.all()
    else:
        # Tratamento de erro seguro caso o perfil de cliente não exista
        cliente = get_object_or_404(Cliente, usuario=request.user)
        pets = Animal.objects.filter(cliente=cliente)
        
    return render(request, 'animal/listar.html', {'pets': pets})

@login_required
def cadastrar_pet(request):
    """Cadastra um novo animal associando-o ao perfil do cliente atual."""
    # Administradores puros não devem cadastrar pets sem estarem associados a um cliente
    if request.user.is_staff and not Cliente.objects.filter(usuario=request.user).exists():
        messages.error(request, 'Administradores precisam de um perfil de cliente para cadastrar pets.')
        return redirect('cliente:dashboard')

    cliente = get_object_or_404(Cliente, usuario=request.user)

    if request.method == 'POST':
        form = AnimalForm(request.POST)
        if form.is_valid():
            # commit=False impede que o Django salve imediatamente no banco, permitindo injetar o cliente antes
            animal = form.save(commit=False)
            animal.cliente = cliente
            animal.save()
            messages.success(request, f'{animal.nome_pet} foi cadastrado com sucesso!')
            return redirect('animal:listar')
    else:
        form = AnimalForm()

    return render(request, 'animal/cadastrar.html', {'form': form})