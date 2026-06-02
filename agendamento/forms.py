from django import forms
from .models import Agendamento
from animal.models import Animal
from servico.models import Servico

class AgendamentoForm(forms.ModelForm):
    # Campo personalizado para exibir múltiplos serviços como checkboxes
    servicos = forms.ModelMultipleChoiceField(
        queryset=Servico.objects.all(),
        widget=forms.CheckboxSelectMultiple(attrs={'class': 'checkbox-servicos'}),
        label="Selecione os Serviços"
    )

    class Meta:
        model = Agendamento
        fields = ['animal', 'data', 'hora', 'servicos']
        widgets = {
            'data': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'hora': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}),
            'animal': forms.Select(attrs={'class': 'form-control'}),
        }

    def __init__(self, *args, **kwargs):
        # Captura o cliente logado enviado pela View para filtrar apenas os pets dele
        cliente = kwargs.pop('cliente', None)
        super().__init__(*args, **kwargs)
        
        if cliente:
            self.fields['animal'].queryset = Animal.objects.filter(cliente=cliente)
            self.fields['animal'].empty_label = "Selecione o seu Pet"