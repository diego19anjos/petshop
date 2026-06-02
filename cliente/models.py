from django.db import models
from django.contrib.auth.models import User

class Cliente(models.Model):
    id_cliente = models.AutoField(primary_key=True, db_column='ID_cliente')
    
    # Vinculo com o sistema de usuários padrão do Django
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, db_column='USER_ID_usuario', null=True, blank=True)
    
    nome_completo = models.CharField(max_length=75)
    cpf_cliente = models.CharField(max_length=11, blank=True, null=True)
    telefone_cliente = models.CharField(max_length=13, blank=True, null=True)
    endereco_cliente = models.CharField(max_length=100, blank=True, null=True)
    email_cliente = models.EmailField(max_length=45)

    class Meta:
        db_table = 'CLIENTE'
        verbose_name = 'Cliente'
        verbose_name_plural = 'Clientes'

    def __str__(self):
        return self.nome_completo