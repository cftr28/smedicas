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

def cita(request):
    es_docente = is_docente(request.user)
    es_superuser = request.user.is_superuser
    return render(request, 'html/cita.html', {'es_docente': es_docente, 'es_superuser': es_superuser})

def about(request):
    es_docente = is_docente(request.user)
    es_superuser = request.user.is_superuser
    return render(request, 'html/about.html', {'es_docente': es_docente, 'es_superuser': es_superuser})

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
