from proyecto_agendamiento.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
     path('contact/', views.contact, name='contact'),
    path('registro_carreras/', views.registro_carreras, name='registro_carreras'),
    path('gestion_carreras/', views.gestion_carreras, name='gestion_carreras'),
    path('eliminar_carrera/<str:nombre>/', views.eliminar_carrera, name='eliminar_carrera'),
    path('modificar_carrera/<str:nombre>/', views.modificar_carrera, name='modificar_carrera'),
    path('registro_asignaturas/', views.registro_asignaturas, name='registro_asignaturas'),
    path('gestion_asignaturas/', views.gestion_asignaturas, name='gestion_asignaturas'),
    path('eliminar_asignatura/<str:nombre>/', views.eliminar_asignatura, name='eliminar_asignatura'),
    path('modificar_asignatura/<str:nombre>/', views.modificar_asignatura, name='modificar_asignatura'),
    path('registro_docentes/', views.registro_docentes, name='registro_docentes'),
    path('gestion_docentes/', views.gestion_docentes, name='gestion_docentes'),
    path('eliminar_docente/<str:correo>/', views.eliminar_docente, name='eliminar_docente'),
    path('modificar_docente/<str:correo>/', views.modificar_docente, name='modificar_docente'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('pedir_tutoria/', views.pedir_tutoria, name='pedir_tutoria'),
    path('aceptar_tutoria/', views.aceptar_tutoria, name='aceptar_tutoria'),
    path('gestionar_registros/', views.gestionar_registros, name='gestionar_registros'),
    path('inicio_estudiante/', views.inicio_estudiante, name='inicio_estudiante'),
    path('confirmacion_envio_email/', views.confirmacion_envio_email, name='confirmacion_envio_email'),
    path('enviar_solicitud/', views.enviar_solicitud, name='enviar_solicitud'),
    path('enviar_solicitud_aceptada_estudiante/',views.enviar_solicitud_aceptada_estudiante, name='enviar_solicitud_aceptada_estudiante'),
    path('enviar_solicitud_rechazada_estudiante/',views.enviar_solicitud_rechazada_estudiante, name='enviar_solicitud_rechazada_estudiante'),
    path('generar_pdf/', views.generar_pdf, name='generar_pdf')
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)