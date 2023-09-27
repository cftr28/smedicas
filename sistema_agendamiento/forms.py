#from django.forms import ModelForm
from django import forms
from .models import *
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class CustomUserCreationForm(UserCreationForm):
    email = forms.EmailField(label="Correo electrónico")
    first_name = forms.CharField(label="Nombre")
    last_name = forms.CharField(label="Apellido")
    
    class Meta:
        model = User
        fields = ['username', 'email', 'first_name', 'last_name', 'password1', 'password2']

class EspecialidadForm(forms.ModelForm):
    class Meta:
        model=Especialidad
        fields='__all__'

class DoctorForm(forms.ModelForm):
    class Meta:
        model=Doctor
        fields='__all__'

class CitaForm(forms.ModelForm):
    class Meta:
        model = Cita
        fields = ['doctor', 'paciente', 'fecha', 'hora']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['hora'].widget = forms.Select(attrs={'class': 'select-hour'})

class PacienteForm(forms.ModelForm):
    class Meta:
        model=Paciente
        fields='__all__'

class CitaPacienteForm(forms.ModelForm):
    class Meta:
        model=CitaPaciente
        fields='__all__'

