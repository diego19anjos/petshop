from django.urls import path
from . import views

app_name = 'animal'

urlpatterns = [
    path('', views.listar_pets, name='listar'),
    path('novo/', views.cadastrar_pet, name='cadastrar'),
]