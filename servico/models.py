from django.db import models

class Servico(models.Model):

    id_servico = models.AutoField(
    primary_key=True,
    db_column='ID_servico'
)

    nome_servico = models.CharField(
        max_length=45
    )

    descricao_servico = models.CharField(
        max_length=45
    )
    preco_servico = models.FloatField()
    duracao_servico = models.IntegerField()

    class Meta:

        db_table = 'SERVICO'
        verbose_name = 'Serviço'
        verbose_name_plural = 'Serviços'

    def __str__(self):

        return self.nome_servico