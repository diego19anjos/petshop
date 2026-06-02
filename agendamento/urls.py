from django.urls import path
from . import views

app_name = 'agendamento'

urlpatterns = [
    path('', views.fazer_agendamento, name='agendamento'),
]