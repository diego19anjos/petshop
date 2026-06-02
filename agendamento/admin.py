from django.contrib import admin
from .models import Agendamento
from .models import AgendamentoServico


admin.site.register(Agendamento)
admin.site.register(AgendamentoServico)