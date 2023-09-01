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
   
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)