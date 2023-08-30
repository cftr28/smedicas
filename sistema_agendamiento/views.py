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
from .models import Estudiante, Asignatura, Docente
from django.http import HttpResponse
from proyecto_agendamiento.settings import EMAIL_HOST_USER
from .forms import *

import os
from django.conf import settings
from django.http import HttpResponse
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib.staticfiles import finders
from io import BytesIO
from urllib.request import urlopen  # Importa urlopen desde urllib.request



# Vistas de las diferentes paginas del proyecto.
def is_docente(user):
    return user.groups.filter(name='Docente').exists()


def index(request):
    es_docente = is_docente(request.user)
    es_superuser = request.user.is_superuser
    return render(request, 'html/index.html', {'es_docente': es_docente, 'es_superuser': es_superuser})

def contact(request):
    es_docente = is_docente(request.user)
    es_superuser = request.user.is_superuser
    return render(request, 'html/contact.html', {'es_docente': es_docente, 'es_superuser': es_superuser})


def about(request):
    es_docente = is_docente(request.user)
    es_superuser = request.user.is_superuser
    return render(request, 'html/about.html', {'es_docente': es_docente, 'es_superuser': es_superuser})




def registro_docentes(request):
    carreras = Carrera.objects.all()
    if request.method == 'POST':
        nombres = request.POST['txtNombre']
        apellidos = request.POST['txtApellido']
        correo = request.POST['txtCorreo']
        carrera_id = request.POST['slCarrera']
        horario = request.FILES.get('txtHorario')
        try:
            carrera = Carrera.objects.get(pk=carrera_id)
            docente = Docente.objects.create(nombres=nombres, apellidos=apellidos, correo=correo, carrera=carrera, horario=horario)
            messages.success(request, 'Docente registrado exitosamente.')
            return redirect("registro_docentes")
        except Exception as e:
            messages.error(request, 'No se pudo registrar el docente: {}'.format(str(e)))
    return render(request, 'html/registro_docentes.html',{"carreras":carreras})


def gestion_docentes(request):
    listaDocentes = Docente.objects.all()
    return render(request, "html/gestion_docentes.html", {"listaDocentes":listaDocentes})


def eliminar_docente(request, correo):
    docente = get_object_or_404(Docente, correo=correo)
    if docente:
        docente.delete()
        messages.success(request, 'Docente eliminado exitosamente')
        return redirect('gestion_docentes')
    else:
        messages.error(request, 'No se pudo eliminar docente')


def modificar_docente(request, correo):
    docente = get_object_or_404(Docente, correo=correo)
    lista_carreras = Carrera.objects.all()
    if request.method == 'POST':
        nuevos_nombres = request.POST['nuevos_nombres']
        nuevos_apellidos = request.POST['nuevos_apellidos']
        nuevo_correo = request.POST['nuevo_correo']
        nuevo_horario = request.FILES['nuevo_horario'] if 'nuevo_horario' in request.FILES else None
        nuevo_carrera_id = request.POST['nuevo_carrera']

        docente.nombres = nuevos_nombres
        docente.apellidos = nuevos_apellidos
        docente.correo = nuevo_correo
        if nuevo_horario:
            docente.horario = nuevo_horario
        docente.carrera_id = nuevo_carrera_id
        docente.save()

        return redirect('gestion_docentes')

    return render(request, 'html/modificar_docente.html', {'docente': docente, 'lista_carreras':lista_carreras})


def registro_asignaturas(request):
    carreras = Carrera.objects.all()
    docentes = Docente.objects.all()
    if request.method == 'POST':
        nombre = request.POST['txtNombreAs']
        ciclo = request.POST['txtCiclo']
        paralelo = request.POST['txtParalelo']
        docente_id = request.POST['slDocente']
        carrera_id = request.POST['slCarrera']
        try:
            docente = Docente.objects.get(pk=docente_id)
            carrera = Carrera.objects.get(pk=carrera_id)
            asignatura = Asignatura.objects.create(nombre=nombre, ciclo=ciclo, paralelo=paralelo,
                                     docente=docente, carrera=carrera)
            messages.success(request, 'Asignatura registrada exitosamente.')
            return redirect("registro_asignaturas")
        except Exception as e:
            messages.error(request, 'No se pudo registrar la asignatura: {}'.format(str(e)))
    return render(request, 'html/registro_asignaturas.html',{"carreras":carreras, "docentes":docentes})


def gestion_asignaturas(request):
    listaAsignaturas = Asignatura.objects.all()
    return render(request, "html/gestion_asignaturas.html", {"listaAsignaturas":listaAsignaturas})


def eliminar_asignatura(request, nombre):
    asignatura = get_object_or_404(Asignatura, nombre=nombre)
    if asignatura:
        asignatura.delete()
        messages.success(request, 'Asignatura eliminada exitosamente')
        return redirect('gestion_asignaturas')
    else:
        messages.error(request, 'No se pudo eliminar asignatura')


def modificar_asignatura(request, nombre):
    asignatura = get_object_or_404(Asignatura, nombre=nombre)
    lista_carreras = Carrera.objects.all()
    lista_docentes = Docente.objects.all()
    if request.method == 'POST':
        nuevo_nombre = request.POST['nuevo_nombre']
        nuevo_ciclo = request.POST['nuevo_ciclo']
        nuevo_paralelo = request.POST['nuevo_paralelo']
        nuevo_carrera_id = request.POST['nuevo_carrera']
        nuevo_docente_id = request.POST['nuevo_docente']

        asignatura.nombre = nuevo_nombre
        asignatura.ciclo = nuevo_ciclo
        asignatura.paralelo = nuevo_paralelo
        asignatura.carrera_id = nuevo_carrera_id
        asignatura.docente_id = nuevo_docente_id
        asignatura.save()

        return redirect('gestion_asignaturas')

    return render(request, 'html/modificar_asignatura.html', {'asignatura': asignatura, 'lista_carreras': lista_carreras, 'lista_docentes': lista_docentes})


def registro_carreras(request):
    carreras = Carrera.objects.all()
    if request.method == 'POST':
        nombre = request.POST['txtNombre']
        facultad = request.POST['slFacultad']
        inicio_periodo = request.POST['txtInicio']
        final_periodo = request.POST['txtFin']
        try:
            carrera = Carrera.objects.create(nombre=nombre, facultad=facultad, inicio_periodo=inicio_periodo,
                            final_periodo=final_periodo)
            messages.success(request, 'Carrera registrada exitosamente.')
            return redirect("registro_carreras")
        except Exception as e:
            messages.error(request, 'No se pudo registrar la carrera: {}'.format(str(e)))
    return render(request, 'html/registro_carreras.html', {"carreras": carreras})


def gestion_carreras(request):
    listaCarrera = Carrera.objects.all()
    return render(request, "html/gestion_carreras.html", {"listaCarrera":listaCarrera})


def eliminar_carrera(request, nombre):
    carrera = get_object_or_404(Carrera, nombre=nombre)
    if carrera:
        carrera.delete()
        messages.success(request, 'Carrera eliminada exitosamente')
        return redirect('gestion_carreras')
    else:
        messages.error(request, 'No se pudo eliminar la carrera')


def modificar_carrera(request, nombre):
    carrera = get_object_or_404(Carrera, nombre=nombre)
    if request.method == 'POST':
        nueva_nombre = request.POST['nueva_nombre']
        nueva_facultad = request.POST['nueva_facultad']
        nueva_inicio = request.POST['nueva_inicio']
        nueva_final = request.POST['nueva_final']

        carrera.nombre = nueva_nombre
        carrera.facultad = nueva_facultad
        carrera.inicio_periodo = nueva_inicio
        carrera.final_periodo = nueva_final
        carrera.save()

        return redirect('gestion_carreras')

    return render(request, 'html/modificar_carrera.html', {'carrera': carrera})


def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            auth_login(request, user)
            return redirect('/')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'html/registro.html', {'form': form})


def login(request):
    if request.method == 'GET':
        return render(request, 'html/iniciosesion.html', {'form': AuthenticationForm()})
    else:
        user = auth_authenticate(username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'html/iniciosesion.html', {'form': AuthenticationForm(), 'error': 'Usuario y/o contraseña incorrectos.'})
        else:
            auth_login(request, user)
            return redirect('/')


def logout(request):
    auth_logout(request)
    return redirect('/')


def pedir_tutoria(request):
    return render(request, 'html/pedir_tutoria.html')


@user_passes_test(is_docente)
def aceptar_tutoria(request):
    user = request.user
    if user.is_authenticated:
        tutorias = Tutoria.objects.filter(asignatura__docente__correo=user.email)
        lista_estudiantes = []

        for tutoria in tutorias:
            #docente = asignatura.docente
            estudiante = tutoria.estudiante
            lista_estudiantes.append(estudiante)
        return render(request, 'html/aceptar_tutoria.html', {'lista_estudiantes': lista_estudiantes})

    return HttpResponse("No tienes permisos para acceder a esta página.")

    #return render(request, 'html/aceptar_tutoria.html', {'es_docente': True, "estudiante": estudiante})
@login_required
def enviar_solicitud_aceptada_estudiante(request):
    #estudiante = Estudiante.objects.all()
    if request.method == 'POST':
        nombre_estudiante = request.POST['txtnombre']
        hora = request.POST['txthora']
        dia = request.POST['txtdia']
        tutoria_info = request.POST['txtinfotutoria']
        correo_estudiante = request.POST['correo_estudiante']

            # Envío de correo electrónico
        subject = f'Solicitud de Tutoría'
        message = f'Estimado/a {nombre_estudiante},\n\nSe ha aceptado su tutoria.\n\nDetalles de la solicitud:\nHora: ' \
                      f'{hora}\nDia:{dia}\nInformación: {tutoria_info}\n'
        from_email = EMAIL_HOST_USER
        recipient_list = [correo_estudiante]

        send_mail(subject, message, from_email, recipient_list)
        messages.success(request, 'Correo enviado exitosamente.')
        #return redirect('html/confirmacion_envio_email.html')

    return render(request, 'html/aceptar_tutoria.html')

def enviar_solicitud_rechazada_estudiante(request):
    if request.method == 'POST':
        nombre_estudiante = request.POST['txtnombre1']
        tutoria_info = request.POST['txttutoria']
        correo_estudiante = request.POST['correo_estudiante1']

            # Envío de correo electrónico
        subject = f'Solicitud de Tutoría'
        message = f'Estimado/a {nombre_estudiante},\n\nSe ha rechazado su tutoria.\n\nDetalles de la solicitud:\n '\
        f' \nInformación: {tutoria_info}\n'
        from_email = EMAIL_HOST_USER
        recipient_list = [correo_estudiante]

        send_mail(subject, message, from_email, recipient_list)
        messages.success(request, 'Correo enviado exitosamente.')
        #return redirect('html/confirmacion_envio_email.html')

    return render(request, 'html/aceptar_tutoria.html')


def gestionar_registros(request):
    return render(request, 'html/gestionar_registros.html')


def inicio_estudiante(request):
    listaMaterias = Estudiante.objects.all()
    return render(request, 'html/inicio_estudiante.html', {"lista":listaMaterias})


@login_required
def pedir_tutoria(request):
    user = request.user
    if user.is_authenticated:
        asignaturas = Asignatura.objects.filter(estudiante__usuario=user.email)
        docentes = []

        for asignatura in asignaturas:
            docente = asignatura.docente
            docentes.append(docente)
        return render(request, 'html/pedir_tutoria.html', {'docentes': docentes})

    return HttpResponse("No tienes permisos para acceder a esta página.")


@login_required
def enviar_solicitud(request):
    user = request.user
    if request.method == 'POST':
        correo_alumno = user.email
        nombre_estudiante = request.POST.get('nombre')
        hora_tutoria = request.POST.get('hora')
        dia_tutoria = request.POST.get('dia')
        informacion_tutoria = request.POST.get('tutoria')
        correo_docente = request.POST.get('correo_docente')
        # ... Resto de tu código ...
        context = {
            'nombre_estudiante': nombre_estudiante,
            'hora_tutoria': hora_tutoria,
            'dia_tutoria': dia_tutoria,
            'informacion_tutoria': informacion_tutoria,
            'correo_alumno': correo_alumno,
        }
        email_content = render_to_string('html/email_template.html', context)

        # Crear y enviar el correo electrónico con formato HTML
        subject = 'Solicitud de Tutoría'
        from_email = EMAIL_HOST_USER
        recipient_list = [correo_docente]

        email = EmailMessage(subject, email_content, from_email, recipient_list)
        email.content_subtype = 'html'  # Indicar que el contenido es HTML
        email.send()
        
        return render(request, 'html/confirmacion_envio_email.html')  # Renderizar una página de éxito o redirigir a donde sea necesario
    
    return render(request, 'html/perdir_tutoria.html')


def confirmacion_envio_email(request):
    return render(request, 'html/confirmacion_envio_email.html')

def fetch_resources(uri, rel):
    # Función de callback para cargar recursos como imágenes
    if uri.startswith("/media/"):  # Reemplaza esto con la ruta correcta
        path = uri.replace("/media/", "")  # Ajusta la ruta según tu estructura de archivos
        return path
    return uri

def generar_pdf(request):
    template = get_template('html/generar_pdf.html')
    context = {
        'tutorias': Tutoria.objects.all()
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

