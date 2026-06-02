from django.shortcuts import render
from .models import Servico

def listar_servicos(request):
    """View pública que exibe todos os serviços ofertados pelo PetShop."""
    servicos = Servico.objects.all()
    return render(request, 'servico/listar.html', {'servicos': servicos})