from  .forms import *
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.contrib.auth import login as auth_login
from django.contrib.auth import logout as auth_logout
from django.contrib.auth import authenticate as auth_authenticate
from django.db import IntegrityError
from django.contrib.auth.decorators import user_passes_test, login_required
from .forms import CustomUserCreationForm
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.decorators import user_passes_test
from .forms import CustomUserCreationForm
from django.contrib import messages
from .models import Paciente, Cita, Doctor, Especialidad, CitaPaciente
from django.http import HttpResponse
from proyecto_agendamiento.settings import EMAIL_HOST_USER
from .forms import *
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from urllib.request import urlopen  # Importa urlopen desde urllib.request
from django.shortcuts import redirect, render
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.core.mail import send_mail
from django.contrib import messages

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart


# Otras importaciones aquí...

def contact(request):
    if request.method == 'POST':
          
        nombre = request.POST['nombre']
        email = request.POST['email']
        contenido = request.POST['contenido']

        # Configuración de los parámetros de conexión SMTP
        servidor_smtp = 'smtp.gmail.com'
        puerto = 587
        usuario = 'sdetutorias@gmail.com'
        contraseña = 'hnlohetxsjpzsqgs'

        # Crear el mensaje de correo
        msg = MIMEMultipart()
        msg['From'] = usuario
        msg['To'] = 'cecilia.trueba@unl.edu.ec'  # Cambia la dirección de correo si es necesario
        msg['Subject'] = 'Mensaje de contacto'
        msg.attach(MIMEText(f'Se ha recibido un mensaje de {nombre},\nCorreo electrónico: {email}.\n\nDetalles del mensaje:\n\n{contenido}', 'plain'))

        # Establecer la conexión SMTP y enviar el correo
        try:
            server = smtplib.SMTP(servidor_smtp, puerto)
            server.starttls()
            server.login(usuario, contraseña)
            server.sendmail(usuario, 'cecilia.trueba@unl.edu.ec', msg.as_string())
            server.quit()
            messages.success(request, 'Correo enviado exitosamente.')

            # Redirigir al usuario a la página de confirmación
            return redirect('confirmar_email')
        except Exception as e:
            messages.error(request, f'Error al enviar el correo: {str(e)}')

    return render(request, 'html/contact.html')

def confirmar_email(request):
    return render(request, 'html/confirmar_email.html')



# Vistas de las diferentes paginas del proyecto.
def is_doctor(user):
    return user.groups.filter(name='Doctor').exists()

def index(request):
    es_doctor = is_doctor(request.user)
    es_superuser = request.user.is_superuser
    return render(request, 'html/index.html', {'es_doctor': es_doctor, 'es_superuser': es_superuser})



def cita(request):
    es_doctor = is_doctor(request.user)
    es_superuser = request.user.is_superuser
    return render(request, 'html/cita.html', {'es_doctor': es_doctor, 'es_superuser': es_superuser})

def about(request):
    es_doctor = is_doctor(request.user)
    es_superuser = request.user.is_superuser
    return render(request, 'html/about.html', {'es_doctor': es_doctor, 'es_superuser': es_superuser})


def registro_doctores(request):
    especialidades = Especialidad.objects.all()
    pacientes = Paciente.objects.all()  # Obtener todos los pacientes

    if request.method == 'POST':
        nombres = request.POST.get('txtNombre')
        apellidos = request.POST.get('txtApellido')
        correo = request.POST.get('txtCorreo')
        especialidad_id = request.POST.get('slEspecialidad')

        try:
            especialidad = Especialidad.objects.get(pk=especialidad_id)
            doctor = Doctor.objects.create(nombres=nombres, apellidos=apellidos, correo=correo, especialidad=especialidad)

            # Registrar pacientes
            pacientes_seleccionados = request.POST.getlist('slPacientes')
            for paciente_id in pacientes_seleccionados:
                paciente = Paciente.objects.get(pk=paciente_id)
                doctor.pacientes.add(paciente)

            messages.success(request, 'Doctor registrado exitosamente.')
            return redirect("registro_doctores")
        except Exception as e:
            messages.error(request, 'No se pudo registrar el doctor: {}'.format(str(e)))

    return render(request, 'html/registro_doctores.html', {"especialidades": especialidades, "pacientes": pacientes})

def gestion_doctores(request):
    listaDoctores = Doctor.objects.all()
    return render(request, "html/gestion_doctores.html", {"listaDoctores":listaDoctores})

def eliminar_doctor(request, nombres):
    doctor = get_object_or_404(Doctor, nombres=nombres)
    if doctor:
        doctor.delete()
        messages.success(request, 'Doctor eliminado exitosamente')
        return redirect('gestion_doctores')
    else:
        messages.error(request, 'No se pudo eliminar doctor')

def modificar_doctor(request, nombres):
    doctor = get_object_or_404(Doctor, nombres=nombres)
    lista_especialidades = Especialidad.objects.all()
    lista_pacientes = Paciente.objects.all()
    
    if request.method == 'POST':
        nuevos_nombres = request.POST.get('nuevos_nombres')
        nuevos_apellidos = request.POST.get('nuevos_apellidos')
        nuevo_correo = request.POST.get('nuevo_correo')
        nuevo_especialidad_id = request.POST.get('nuevo_especialidad')
        nuevos_pacientes_ids = request.POST.getlist('nuevo_paciente')
        
        doctor.nombres = nuevos_nombres
        doctor.apellidos = nuevos_apellidos
        doctor.correo = nuevo_correo

        if nuevo_especialidad_id:
            especialidad = get_object_or_404(Especialidad, pk=nuevo_especialidad_id)
            doctor.especialidad = especialidad

        # Limpiar y agregar nuevos pacientes
        doctor.pacientes.clear()
        for paciente_id in nuevos_pacientes_ids:
            paciente = get_object_or_404(Paciente, pk=paciente_id)
            doctor.pacientes.add(paciente)

        doctor.save()

        return redirect('gestion_doctores')

    return render(request, 'html/modificar_doctor.html', {'doctor': doctor, 'lista_especialidades': lista_especialidades, 'lista_pacientes': lista_pacientes})

def registro_especialidades(request):
    especialidades = Especialidad.objects.all()
    if request.method == 'POST':
        nombre = request.POST['txtNombre']
        try:
            nueva_especialidad = Especialidad.objects.create(nombre=nombre)
            messages.success(request, 'Especialidad registrada exitosamente.')
            return redirect("registro_especialidades")
        except Exception as e:
            messages.error(request, 'No se pudo registrar la especialidad: {}'.format(str(e)))
    return render(request, 'html/registro_especialidades.html', {"especialidades": especialidades})

def gestion_especialidades(request):
    listaespecialidad = Especialidad.objects.all()
    return render(request, "html/gestion_especialidades.html", {"listaespecialidad":listaespecialidad})

def eliminar_especialidad(request, nombre):
    especialidad = get_object_or_404(Especialidad, nombre=nombre)
    if  especialidad:
        especialidad.delete()
        messages.success(request, ' especialidad eliminada exitosamente')
        return redirect('gestion_especialidades')
    else:
        messages.error(request, 'No se pudo eliminar la  especialidad')

def modificar_especialidad(request, nombre):
    especialidad = get_object_or_404(Especialidad, nombre=nombre)
    if request.method == 'POST':
        nueva_nombre = request.POST['nueva_nombre']

        especialidad.nombre = nueva_nombre
        especialidad.save()

        return redirect('gestion_especialidades')

    return render(request, 'html/modificar_especialidad.html', {' especialidad':  especialidad})

def registro_citas(request):
    doctores = Doctor.objects.all()
    pacientes = Paciente.objects.all()
    
    if request.method == 'POST':
        doctor_id = request.POST.get('txtDoctor')
        paciente_id = request.POST.get('txtPaciente')
        fecha = request.POST.get('txtFecha')
        hora = request.POST.get('txtHora')
        
        try:
            doctor = Doctor.objects.get(pk=doctor_id)
            paciente = Paciente.objects.get(pk=paciente_id)
            
            cita = Cita.objects.create(doctor=doctor, paciente=paciente, fecha=fecha, hora=hora)
            messages.success(request, 'Cita registrada exitosamente.')
            return redirect("registro_citas")
        except Exception as e:
            messages.error(request, 'No se pudo registrar la cita: {}'.format(str(e)))
    
    return render(request, 'html/registro_citas.html', {"doctores": doctores, "pacientes": pacientes})


def gestion_citas(request):
    listacitas = Cita.objects.all()
    return render(request, "html/gestion_citas.html", {"listacitas":listacitas})

def eliminar_citas(request, hora):
    citas = get_object_or_404(Cita, hora=hora)
    if  citas:
        citas.delete()
        messages.success(request, ' cita eliminada exitosamente')
        return redirect('gestion_citas')
    else:
        messages.error(request, 'No se pudo eliminar la cita')


def modificar_citas(request, hora):
    citas = get_object_or_404(Cita, hora=hora)
    lista_doctores = Doctor.objects.all()
    lista_pacientes = Paciente.objects.all()
    
    if request.method == 'POST':
        nueva_doctor_id = request.POST['nueva_doctor']
        nueva_paciente_id = request.POST['nueva_paciente']
        nueva_hora = request.POST['nueva_hora']
        nueva_fecha = request.POST['nueva_fecha']
        
        citas.doctor = lista_doctores.get(pk=nueva_doctor_id)
        citas.paciente = lista_pacientes.get(pk=nueva_paciente_id)
        citas.hora = nueva_hora
        citas.fecha = nueva_fecha
        citas.save()
        
        return redirect('gestion_citas')
    
    return render(request, 'html/modificar_citas.html', {'citas': citas, 'lista_doctores': lista_doctores, 'lista_pacientes': lista_pacientes})

def registro_pacientes(request):
    # Obtén la lista de pacientes existentes
    pacientes = Paciente.objects.all()

    if request.method == 'POST':
        nombre = request.POST['txtnombre']
        apellido = request.POST['txtapellido']
        usuario = request.POST['txtusuario']
        clave = request.POST['txtclave']
        sexo = request.POST['slsexo']
    
        try:
            # Crea un nuevo paciente y guárdalo en la base de datos
            nuevo_paciente = Paciente(nombre=nombre, apellido=apellido, usuario=usuario, clave=clave, sexo=sexo)
            nuevo_paciente.save()

            messages.success(request, 'Paciente registrado exitosamente.')
            return redirect("registro_pacientes")
        except Exception as e:
            messages.error(request, 'No se pudo registrar al paciente: {}'.format(str(e)))
    
    return render(request, 'html/registro_pacientes.html', {"pacientes": pacientes})


def gestion_pacientes(request):
    listapacientes = Paciente.objects.all()
    return render(request, "html/gestion_pacientes.html", {"listapacientes":listapacientes})

def eliminar_pacientes(request, nombre):
    pacientes = get_object_or_404(Paciente, nombre=nombre)
    if  pacientes:
        pacientes.delete()
        messages.success(request, ' paciente eliminado exitosamente')
        return redirect('gestion_pacientes')
    else:
        messages.error(request, 'No se pudo eliminar al paciente')

from django.shortcuts import get_object_or_404

def modificar_pacientes(request, nombre):
    paciente = get_object_or_404(Paciente, nombre=nombre)  # Cambiar "pacientes" a "paciente"
    
    if request.method == 'POST':
        nueva_nombre = request.POST['nueva_nombre']
        nueva_apellido = request.POST['nueva_apellido']
        nueva_usuario = request.POST['nueva_usuario']
        nueva_clave = request.POST['nueva_clave']
        nueva_sexo = request.POST['nueva_sexo']
        
        # Actualizar los campos del paciente
        paciente.nombre = nueva_nombre
        paciente.apellido = nueva_apellido
        paciente.usuario = nueva_usuario
        paciente.clave = nueva_clave
        paciente.sexo = nueva_sexo
        
        paciente.save()  # Guardar los cambios

        return redirect('gestion_pacientes')

    return render(request, 'html/modificar_pacientes.html', {'paciente': paciente})  # Cambiar 'pacientes' a 'paciente' en el contexto


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'html/register.html', {'form': form})

def login(request):
    if request.method == 'GET':
        return render(request, 'html/login.html', {'form': AuthenticationForm()})
    else:
        user = auth_authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'html/login.html', {'form': AuthenticationForm(), 'error': 'Usuario y/o contraseña incorrectos.'})
        else:
            auth_login(request, user)
            return redirect('/')
        
def logout(request):
    auth_logout(request)
    return redirect('/')



@login_required
def enviar_solicitud_aceptada_paciente(request):
    #est
    if request.method == 'POST':
        nombre_paciente = request.POST['txtnombre']
        hora = request.POST['txthora']
        dia = request.POST['txtdia']
        cita_info = request.POST['txtinfocita']
        correo_paciente= request.POST['correo_paciente']

            # Envío de correo electrónico
        subject = f'Solicitud de Cita'
        message = f'Estimado/a {nombre_paciente},\n\nSe ha aceptado su cita.\n\nDetalles de la solicitud:\nHora: ' \
                      f'{hora}\nDia:{dia}\nInformación: {cita_info}\n'
        from_email = EMAIL_HOST_USER
        recipient_list = [correo_paciente]

        send_mail(subject, message, from_email, recipient_list)
        messages.success(request, 'Correo enviado exitosamente.')
        #return redirect('html/confirmacion_envio_email.html')

    return render(request, 'html/aceptar_cita.html')



def gestionar_registros(request):
    return render(request, 'html/gestionar_registros.html')

def inicio_paciente(request):
    listapaciente = Paciente.objects.all()
    return render(request, 'html/inicio_paciente.html', {"lista":listapaciente})


def fetch_resources(uri, rel):
    # Función de callback para cargar recursos como imágenes
    if uri.startswith("/media/"):  # Reemplaza esto con la ruta correcta
        path = uri.replace("/media/", "")  # Ajusta la ruta según tu estructura de archivos
        return path
    return uri

def generar_pdf(request):
    template = get_template('html/generar_pdf.html')
    context = {
        'citas': Cita.objects.all()
    }
    
    html = template.render(context)
    response = HttpResponse(content_type='application/pdf')
    #response['Content-Disposition'] = 'attachment; filename="registroacademico.pdf"'
    # Configura la ruta de imágenes (PYTHON_HTML2PDF_IMAGES)
    pdf_options = {
        "images": True,
    }
    pisa_status = pisa.CreatePDF(html, dest=response, link_callback=fetch_resources, **pdf_options)

     # create a pdf
    #pisa_status = pisa.CreatePDF(
    #    html, dest=response)

    if pisa_status.err:
        return HttpResponse('Error al generar PDF', content_type='text/plain')           
    return response


def citapaciente(request):
    if request.method == 'POST':
        nombre = request.POST['nombre']
        correo = request.POST['correo']
        telefono = request.POST['telefono']
        cedula = request.POST['cedula']
        fecha = request.POST['fecha']
        hora = request.POST['hora']

        # Configuración de los parámetros de conexión SMTP
        servidor_smtp = 'smtp.gmail.com'
        puerto = 587
        usuario = 'sdetutorias@gmail.com'
        contraseña = 'hnlohetxsjpzsqgs'

        # Crear el mensaje de correo
        msg = MIMEMultipart()
        msg['From'] = usuario
        msg['To'] = correo + ', cecilia.trueba@unl.edu.ec'  # Concatena los correos con comas
        msg['Subject'] = 'Nueva cita médica registrada'
        msg.attach(MIMEText(f'Nombre: {nombre}\nCorreo: {correo}\nTeléfono: {telefono}\nCédula: {cedula}\nFecha: {fecha}\nHora: {hora}', 'plain'))

        # Establecer la conexión SMTP y enviar el correo
        try:
            server = smtplib.SMTP(servidor_smtp, puerto)
            server.starttls()
            server.login(usuario, contraseña)
            server.sendmail(usuario, [correo, 'cecilia.trueba@unl.edu.ec'], msg.as_string())
            server.quit()

            # Guardar los datos en la base de datos
            cita = CitaPaciente(nombre=nombre, correo=correo, telefono=telefono, cedula=cedula, fecha=fecha, hora=hora)
            cita.save()

            messages.success(request, 'Correo enviado y cita registrada exitosamente.')

            # Redirigir al usuario a la página de confirmación
            return redirect('confirmarcita')

        except Exception as e:
            messages.error(request, f'Error al enviar el correo o registrar la cita: {str(e)}')

    return render(request, 'html/cita.html')

def confirmarcita(request):
    return render(request, 'html/confirmarcita.html')