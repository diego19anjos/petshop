from django.urls import path
from . import views

app_name = 'cliente'

urlpatterns = [
    # Se o usuário acessar /dashboard/ sem especificar, nossa view global decide o direcionamento
    path('', views.dashboard_cliente, name='dashboard'), 
    
    # Rotas específicas separadas por arquitetura
    path('cliente/', views.dashboard_cliente, name='dashboard_cliente'),
    path('admin/', views.dashboard_admin, name='dashboard_admin'),
    
    # Rota dinâmica para o funcionário concluir ou cancelar serviços clicando no painel
    path('agendamento/<int:agendamento_id>/status/<str:novo_status>/', views.alterar_status_agendamento, name='alterar_status'),
]