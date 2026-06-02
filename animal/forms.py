from django import forms
from .models import Animal

class AnimalForm(forms.ModelForm):
    class Meta:
        model = Animal
        # Não colocamos 'cliente' aqui porque vamos associar o pet ao usuário logado na View de forma automática e segura.
        fields = ['nome_pet', 'especie', 'raca', 'data_nascimento', 'peso', 'observacoes']
        
        widgets = {
            'nome_pet': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nome do Pet'}),
            'especie': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Cachorro, Gato'}),
            'raca': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Ex: Poodle, Vira-lata'}),
            'data_nascimento': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'peso': forms.NumberInput(attrs={'class': 'form-control', 'step': '0.1', 'placeholder': 'Peso em kg'}),
            'observacoes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Alguma restrição ou cuidado especial?'}),
        }