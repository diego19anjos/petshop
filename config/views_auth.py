import json
from django.http import JsonResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login

from cliente.models import Cliente


def api_cadastro(request):

    if request.method == 'POST':

        dados = json.loads(request.body)

        nome = dados.get('nome')
        email = dados.get('email')
        senha = dados.get('senha')

        if User.objects.filter(username=email).exists():

            return JsonResponse({
                'erro': 'Email já cadastrado'
            }, status=400)

        usuario = User.objects.create_user(
            username=email,
            email=email,
            password=senha,
            first_name=nome
        )

        Cliente.objects.create(
            usuario=usuario,
            nome_completo=nome,
            email_cliente=email
        )

        return JsonResponse({
            'mensagem': 'Cadastro realizado'
        })

    return JsonResponse({'erro': 'Método inválido'})


def api_login(request):

    if request.method == 'POST':

        dados = json.loads(request.body)

        email = dados.get('email')
        senha = dados.get('senha')

        usuario = authenticate(
            username=email,
            password=senha
        )

        if usuario:

            login(request, usuario)

            return JsonResponse({
                'sucesso': True
            })

        return JsonResponse({
            'erro': 'Login inválido'
        }, status=401)

    return JsonResponse({
        'erro': 'Método inválido'
    })