from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from cliente.models import Cliente

def index(request):
    """View para renderizar a página inicial pública."""
    return render(request, 'index.html')

def autenticacao_view(request):
    """View unificada para processar Login e Cadastro (Sign-in / Sign-up)."""
    if request.user.is_authenticated:
        return redirect('cliente:dashboard')

    if request.method == 'POST':
        # Identifica qual formulário foi submetido usando o nome do botão/input de submit
        action = request.POST.get('action')

        # ---------------- LOGIC DE LOGIN ----------------
        if action == 'login':
            email = request.POST.get('email', '').strip()
            senha = request.POST.get('password', '')

            if not email or not senha:
                messages.error(request, 'Por favor, preencha todos os campos.')
                return render(request, 'login.html')

            # O Django por padrão autentica usando 'username'. 
            # Como seu formulário pede Email, vamos buscar o username atrelado a esse email.
            try:
                user_obj = User.objects.get(email=email)
                username = user_obj.username
            except User.DoesNotExist:
                username = None

            user = authenticate(request, username=username, password=senha)

            if user is not None:
                login(request, user)
                messages.success(request, f'Bem-vindo de volta, {user.first_name or user.username}!')
                return redirect('cliente:dashboard')
            else:
                messages.error(request, 'E-mail ou senha incorretos.')

        # ---------------- LÓGICA DE CADASTRO ----------------
        elif action == 'cadastro':
            nome = request.POST.get('nome', '').strip()
            email = request.POST.get('email', '').strip()
            senha = request.POST.get('password', '')

            if not nome or not email or not senha:
                messages.error(request, 'Todos os campos de cadastro são obrigatórios.')
                return render(request, 'login.html')

            if User.objects.filter(email=email).exists():
                messages.error(request, 'Este e-mail já está cadastrado em nosso sistema.')
                return render(request, 'login.html')

            # Criação do User padrão do Django (Usaremos o email como username para simplificar)
            username = email
            # Divide o nome para salvar First/Last name se desejar
            nomes = nome.split(' ', 1)
            first_name = nomes[0]
            last_name = nomes[1] if len(nomes) > 1 else ''

            user = User.objects.create_user(
                username=username,
                email=email,
                password=senha,
                first_name=first_name,
                last_name=last_name
            )

            # CRUCIAL: Criar o perfil de Cliente associado a este usuário
            Cliente.objects.create(
                usuario=user,
                nome_completo=nome,
                email_cliente=email
            )

            # Autentica e loga o usuário automaticamente após se cadastrar
            user_autenticado = authenticate(request, username=username, password=senha)
            if user_autenticado:
                login(request, user_autenticado)
                messages.success(request, 'Conta criada com sucesso! Seja bem-vindo.')
                return redirect('cliente:dashboard')

    return render(request, 'login.html')

def logout_view(request):
    """View para realizar o logout seguro do usuário."""
    logout(request)
    messages.info(request, 'Você saiu da sua conta.')
    return redirect('index')