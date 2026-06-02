from django.urls import path
from . import views

app_name = 'servico'

urlpatterns = [
    path('', views.listar_servicos, name='listar'),
]