# Create your models here.
from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

class Carrera(models.Model):
    OPCIONES_FACULTAD = ( 
        ('Agropecuaria y de Recursos Naturales Renovables', 'Agropecuaria y de Recursos Naturales Renovables'),
        ('Educación, el Arte y la Comunicación', 'Educación, el Arte y la Comunicación'),
        ('Energía, las Industrias y los Recursos Naturales no Renovables', 'Energía, las Industrias y los Recursos Naturales no Renovables'),
        ('Jurídica, Social y Administrativa', 'Jurídica, Social y Administrativa'),
        ('Salud Humana', 'Salud Humana'),
        ('Unidad de Educación a Distancia y en Línea', 'Unidad de Educación a Distancia y en Línea'),
    )

    nombre = models.CharField(max_length=60)
    facultad = models.CharField(max_length=70, choices=OPCIONES_FACULTAD)
    inicio_periodo = models.DateField()
    final_periodo = models.DateField()

    def info_carrera(self):
        return "|{}|{}| periodo: {} hasta {}".format(self.nombre, self.facultad, self.inicio_periodo,
                                                     self.final_periodo)

    def __str__(self):
        return self.info_carrera()


class Docente(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, default=0)
    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    horario = models.ImageField(upload_to='media/', null=True, blank=True)

    def info_docente(self):
        return "|{} {}| - {}".format(self.nombres, self.apellidos, self.carrera)

    def __str__(self):
        return self.info_docente()


class Asignatura(models.Model):
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, default=0)
    docente = models.ForeignKey(Docente, on_delete=models.CASCADE, default=0)
    nombre = models.CharField(max_length=60)
    ciclo = models.CharField(max_length=20)
    paralelo = models.CharField(max_length=5)

    def info_asignatura(self):
        return "{} - {} - {} - {}".format(self.nombre, self.docente.nombres, self.ciclo, self.paralelo)

    def __str__(self):
        return self.info_asignatura()


class Estudiante(models.Model):
    OPCION_SEXO = [
        ('Masculino', 'Masculino'),
        ('Femenino', 'Femenino')
    ]
    nombre = models.CharField(max_length=50)
    apellido = models.CharField(max_length=50)
    usuario = models.EmailField(unique=True)
    clave = models.CharField(max_length=15)
    sexo = models.CharField(max_length=15, choices=OPCION_SEXO, default='F')
    carrera = models.ForeignKey(Carrera, on_delete=models.CASCADE, default=0)
    asignatura=models.ManyToManyField(Asignatura)

    def info_estudiante(self):
        asignaturas_nombres = ', '.join(self.asignatura.values_list('nombre', flat=True))
        return "|{} {}| - |{}| - |{}|".format(self.nombre, self.apellido, self.usuario, asignaturas_nombres)

    def __str__(self):
        return self.info_estudiante()


class Tutoria(models.Model):
    OPCIONES_MODALIDAD = (
        ('presencial', 'Presencial'),
        ('virtual', 'Virtual'),
    )
    #docente = models.OneToOneField(Docente, on_delete=models.CASCADE)
    estudiante = models.ForeignKey(Estudiante, on_delete=models.CASCADE)
    asignatura = models.ForeignKey(Asignatura, on_delete=models.CASCADE)
    horario = models.DateField(auto_now=True)
    tema = models.CharField(max_length=60)
    modalidad = models.CharField(max_length=20, choices=OPCIONES_MODALIDAD, default='presencial')

    def info_tutoria(self):
        return "{} - {} - {} - {} - {}".format(self.tema, self.horario, self.modalidad, self.asignatura.docente.nombres,
                                               self.estudiante.nombre)

    def __str__(self):
        return self.info_tutoria()
    