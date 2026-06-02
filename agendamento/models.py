from django.db import models

from animal.models import Animal
from servico.models import Servico


class Agendamento(models.Model):

    STATUS_CHOICES = (
        ('Agendado', 'Agendado'),
        ('Concluído', 'Concluído'),
        ('Cancelado', 'Cancelado'),
    )

    id_agendamento = models.AutoField(
        primary_key=True,
        db_column='ID_agendamento'
    )

    data = models.DateField()

    hora = models.TimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Agendado'
    )

    valor_total = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        default=0
    )

    animal = models.ForeignKey(
        Animal,
        on_delete=models.CASCADE,
        db_column='ANIMAL_ID_animal',
        related_name='agendamentos'
    )

    servicos = models.ManyToManyField(
        Servico,
        through='AgendamentoServico'
    )

    class Meta:
        db_table = 'AGENDAMENTO'
        verbose_name = 'Agendamento'
        verbose_name_plural = 'Agendamentos'

    def __str__(self):
        return f'{self.animal} - {self.data} {self.hora}'


class AgendamentoServico(models.Model):

    agendamento = models.ForeignKey(
        Agendamento,
        on_delete=models.CASCADE,
        db_column='AGENDAMENTO_ID_agendamento'
    )

    servico = models.ForeignKey(
        Servico,
        on_delete=models.CASCADE,
        db_column='SERVICO_ID_servico'
    )

    class Meta:
        db_table = 'AGENDAMENTO_SERVICO'
        verbose_name = 'Agendamento Serviço'
        verbose_name_plural = 'Agendamentos Serviços'