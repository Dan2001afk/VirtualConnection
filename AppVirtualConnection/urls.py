from django.urls import path
from .views import *
from .viewsLogin import *
from django.urls import path
from . import views
from . import viewsLogin
urlpatterns=[
        
        path('',Inicio,name="InicioPage"),
        path('Inicio',Inicio,name="InicioPage"),
        path('Dashboard/',Dashboard,name="DashboardPage"),
        path('Dispositivos/',Dispositivos,name="DispositivosPage"),
        path('Estadisticas/',Estadisticas,name="EstadisticasPage"),
        path('Alarmas/',Alarmas,name="AlarmasPage"),
        path('Tableros/',Tableros,name="TablerosPage"),
        path('Productos/',Productos,name="ProductosPage"),


        #Autenticacion
        path('IniciarSesion/', viewsLogin.login_with_firebase, name='login'),
        path('RegistrarUsuarios/', viewsLogin.registro_usuario, name='Registro'),

        #graficos

]       