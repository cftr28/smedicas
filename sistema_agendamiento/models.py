from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Especialidad(models.Model):

    nombre = models.CharField(max_length=60)

    def __str__(self):
        return self.nombre

class Paciente(models.Model):
    OPCION_SEXO = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino')
    ]
    
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    usuario = models.EmailField(unique=True)
    clave = models.CharField(max_length=15)
    sexo = models.CharField(max_length=15, choices=OPCION_SEXO)
 

    def __str__(self):
        return f'{self.nombre} {self.apellido}'


class Doctor(models.Model):
    especialidad = models.ForeignKey(Especialidad, on_delete=models.CASCADE)
    
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    pacientes = models.ManyToManyField('Paciente')

    def __str__(self):
        return f'{self.nombres} {self.apellidos}'

class Cita(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    paciente = models.ForeignKey(Paciente, on_delete=models.CASCADE)
    fecha = models.DateField()
    hora = models.TimeField()

    def __str__(self):
        return f'Cita con el Dr. {self.doctor} el {self.fecha} a las {self.hora}'
    
class CitaPaciente(models.Model):
    nombre = models.CharField(max_length=100)
    correo = models.EmailField(unique=False) 
    telefono = models.CharField(max_length=100)
    cedula = models.CharField(max_length=100)
    fecha = models.DateField()
    hora = models.TimeField() 

    def __str__(self):
        return f'Cita con el paciente {self.nombre } el {self.fecha} a las {self.hora}'