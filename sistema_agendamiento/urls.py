from proyecto_agendamiento.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
urlpatterns = [
    path('index/', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('cita/', views.cita, name='cita'),
    path('cita/', views.cita, name='cita'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),

    path('registro_citas/', views.registro_citas, name='registro_citas'),
    path('gestion_citas/', views.gestion_citas, name='gestion_citas'),
    path('eliminar_citas/<str:hora>/', views.eliminar_citas, name='eliminar_citas'),
    path('modificar_citas/<str:hora>/', views.modificar_citas, name='modificar_citas'),
    path('registro_doctores/', views.registro_doctores, name='registro_doctores'),
    path('gestion_doctores/', views.gestion_doctores, name='gestion_doctores'),
    path('eliminar_doctor/<str:nombres>/', views.eliminar_doctor, name='eliminar_doctor'),
    path('modificar_doctor/<str:nombres>/', views.modificar_doctor, name='modificar_doctor'),
    path('registro_pacientes/', views.registro_pacientes, name='registro_pacientes'),
    path('gestion_pacientes/', views.gestion_pacientes, name='gestion_pacientes'),
    path('eliminar_pacientes/<str:nombre>/', views.eliminar_pacientes, name='eliminar_pacientes'),
    path('modificar_pacientes/<str:nombre>/', views.modificar_pacientes, name='modificar_pacientes'),
    path('registro_especialidades/', views.registro_especialidades, name='registro_especialidades'),
    path('gestion_especialidades/', views.gestion_especialidades, name='gestion_especialidades'),
    path('eliminar_especialidad/<str:nombre>/', views.eliminar_especialidad, name='eliminar_especialidad'),
    path('modificar_especialidad/<str:nombre>/', views.modificar_especialidad, name='modificar_especialidad'),
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)