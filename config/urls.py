from django.contrib import admin
from django.urls import path, include
from config.views import index, autenticacao_view, logout_view

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('', index, name='index'),
    path('login/', autenticacao_view, name='login'),
    path('logout/', logout_view, name='logout'),
    
    path('dashboard/', include('cliente.urls')),
    path('animais/', include('animal.urls')),
    path('servicos/', include('servico.urls')),
    path('agendamentos/', include('agendamento.urls')), 
]