from django.contrib import admin
from .models import *
from .models import Especialidad, Doctor,Paciente,Cita,CitaPaciente

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    pass

@admin.register(Especialidad)
class EspecialidadAdmin(admin.ModelAdmin):
    pass

@admin.register(Paciente)
class PacienteAdmin(admin.ModelAdmin):
    pass

@admin.register(Cita)
class CitaAdmin(admin.ModelAdmin):
    pass

@admin.register(CitaPaciente)
class CitaPacienteAdmin(admin.ModelAdmin):
    pass