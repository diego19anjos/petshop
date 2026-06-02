from django.db import models
from cliente.models import Cliente

class Animal(models.Model):

    id_animal = models.AutoField(primary_key=True,db_column='ID_animal')
    nome_pet = models.CharField(max_length=45, db_column='Nome_pet')
    raca = models.CharField(max_length=45, db_column='Raca')
    especie = models.CharField(max_length=45, db_column='Especie')
    data_nascimento = models.DateField(db_column='Data_nascimento')
    peso = models.FloatField(db_column='Peso')
    imagem = models.CharField(max_length=45, null=True, blank=True, db_column='Foto_perfil')
    observacoes = models.CharField(max_length=255,null=True,blank=True,db_column='Observacoes')
    cliente = models.ForeignKey(Cliente,on_delete=models.CASCADE,db_column='CLIENTE_ID_cliente')

    class Meta:

        db_table = 'ANIMAL'

    def __str__(self):

        return self.nome_pet